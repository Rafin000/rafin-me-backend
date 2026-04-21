import secrets
from datetime import datetime, timedelta

from flask import request, current_app as app
from flask_restx import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message

from project.server import bcrypt, db, mail, limiter
from project.server.api.auth import ns_auth
from project.server.api.auth.schema import (
    login_model,
    forgot_password_model,
    reset_password_model,
    update_me_model,
)
from project.server.models.models import Users
from project.server.utils import error_response


RESET_CODE_TTL_MINUTES = 15


def _normalize_email(value):
    return (value or '').strip().lower()


class LoginResource(Resource):
    @ns_auth.expect(login_model, validate=True)
    @ns_auth.response(200, "Login successful")
    @ns_auth.response(401, "Invalid credentials")
    def post(self):
        try:
            data = request.get_json() or {}
            email = _normalize_email(data.get('email'))
            password = data.get('password') or ''

            if not email or not password:
                return error_response(401, "Invalid credentials")

            user = Users.query.filter_by(email=email).first()
            if not user or not user.password_hash:
                return error_response(401, "Invalid credentials")

            if not bcrypt.check_password_hash(user.password_hash, password):
                return error_response(401, "Invalid credentials")

            token = create_access_token(identity=str(user.id))
            return {
                "access_token": token,
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                }
            }, 200
        except Exception as e:
            app.logger.error(f"Login error: {e}")
            return error_response(401, "Invalid credentials")


class MeResource(Resource):
    @jwt_required()
    @ns_auth.response(200, "Current user")
    @ns_auth.response(401, "Unauthorized")
    def get(self):
        user_id = get_jwt_identity()
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return error_response(404, "User not found")
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "designation": user.designation,
        }, 200

    @jwt_required()
    @ns_auth.expect(update_me_model, validate=True)
    @ns_auth.response(200, "Updated")
    @ns_auth.response(400, "Bad request")
    @ns_auth.response(401, "Unauthorized")
    @ns_auth.response(409, "Email already in use")
    def patch(self):
        user_id = get_jwt_identity()
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return error_response(404, "User not found")

        data = request.get_json() or {}
        new_email = data.get('email')
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if new_email is not None:
            email = _normalize_email(new_email)
            if not email or '@' not in email:
                return error_response(400, "Invalid email")
            existing = Users.query.filter(Users.email == email, Users.id != user.id).first()
            if existing:
                return error_response(409, "Email already in use")
            user.email = email

        if new_password:
            if not current_password or not user.password_hash:
                return error_response(400, "Current password required")
            if not bcrypt.check_password_hash(user.password_hash, current_password):
                return error_response(401, "Current password is incorrect")
            if len(new_password) < 8:
                return error_response(400, "Password must be at least 8 characters")
            user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

        db.session.commit()
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "designation": user.designation,
        }, 200


class ForgotPasswordResource(Resource):
    decorators = [limiter.limit('5 per hour; 20 per day')]

    @ns_auth.expect(forgot_password_model, validate=True)
    @ns_auth.response(200, "If the email exists, a code has been sent")
    @ns_auth.response(429, "Too many requests")
    def post(self):
        data = request.get_json() or {}
        email = _normalize_email(data.get('email'))
        generic_ok = {"status": "success", "message": "If the email exists, a reset code has been sent"}

        if not email:
            return generic_ok, 200

        user = Users.query.filter_by(email=email).first()
        if not user:
            return generic_ok, 200

        code = f"{secrets.randbelow(1_000_000):06d}"
        user.reset_code_hash = bcrypt.generate_password_hash(code).decode('utf-8')
        user.reset_code_expires_at = datetime.utcnow() + timedelta(minutes=RESET_CODE_TTL_MINUTES)

        try:
            default_sender = app.config.get('MAIL_DEFAULT_SENDER')
            if not default_sender:
                app.logger.error('MAIL_DEFAULT_SENDER not configured; cannot send reset code')
                return error_response(500, "Mail service not configured")

            msg = Message(
                subject="[rafin.dev] Password reset code",
                sender=("rafin.dev admin", default_sender),
                recipients=[email],
                body=(
                    f"Your admin password reset code is: {code}\n\n"
                    f"It expires in {RESET_CODE_TTL_MINUTES} minutes.\n"
                    "If you did not request this, you can ignore this email."
                ),
            )
            mail.send(msg)
            db.session.commit()
        except Exception as e:
            app.logger.error(f"Failed to send reset email: {e}")
            db.session.rollback()
            return error_response(500, "Unable to send reset email")

        return generic_ok, 200


class ResetPasswordResource(Resource):
    decorators = [limiter.limit('10 per hour; 30 per day')]

    @ns_auth.expect(reset_password_model, validate=True)
    @ns_auth.response(200, "Password reset")
    @ns_auth.response(400, "Invalid or expired code")
    def post(self):
        data = request.get_json() or {}
        email = _normalize_email(data.get('email'))
        code = (data.get('code') or '').strip()
        new_password = data.get('new_password') or ''

        if not email or not code or len(new_password) < 8:
            return error_response(400, "Invalid request")

        user = Users.query.filter_by(email=email).first()
        if not user or not user.reset_code_hash or not user.reset_code_expires_at:
            return error_response(400, "Invalid or expired code")

        if datetime.utcnow() > user.reset_code_expires_at:
            user.reset_code_hash = None
            user.reset_code_expires_at = None
            db.session.commit()
            return error_response(400, "Invalid or expired code")

        if not bcrypt.check_password_hash(user.reset_code_hash, code):
            return error_response(400, "Invalid or expired code")

        user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.reset_code_hash = None
        user.reset_code_expires_at = None
        db.session.commit()

        return {"status": "success", "message": "Password has been reset"}, 200


ns_auth.add_resource(LoginResource, '/login')
ns_auth.add_resource(MeResource, '/me')
ns_auth.add_resource(ForgotPasswordResource, '/forgot-password')
ns_auth.add_resource(ResetPasswordResource, '/reset-password')
