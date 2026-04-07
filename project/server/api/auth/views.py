from flask import request, current_app as app
from flask_restx import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from project.server import bcrypt
from project.server.api.auth import ns_auth
from project.server.api.auth.schema import login_model
from project.server.models.models import Users
from project.server.utils import error_response


class LoginResource(Resource):
    @ns_auth.expect(login_model, validate=True)
    @ns_auth.response(200, "Login successful")
    @ns_auth.response(401, "Invalid credentials")
    def post(self):
        try:
            data = request.get_json()
            username = (data.get('username') or '').strip()
            password = data.get('password') or ''

            user = Users.query.filter_by(username=username).first()
            if not user or not user.password_hash:
                return error_response(401, "Invalid credentials")

            if not bcrypt.check_password_hash(user.password_hash, password):
                return error_response(401, "Invalid credentials")

            token = create_access_token(identity=str(user.id))
            return {
                "access_token": token,
                "user": {
                    "id": str(user.id),
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
            "full_name": user.full_name,
            "designation": user.designation,
        }, 200


ns_auth.add_resource(LoginResource, '/login')
ns_auth.add_resource(MeResource, '/me')
