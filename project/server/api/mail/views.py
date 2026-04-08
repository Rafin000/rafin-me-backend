from flask import request
from flask import current_app as app
from flask_restx import Resource
from flask_mail import Message

from project.server import mail, limiter
from project.server.api.mail import ns_mail
from project.server.api.mail.schema import mail_model
from project.server.utils import error_response


class MailResource(Resource):
    # Per-IP rate limit to stop someone bursting the contact form.
    # The limits are cumulative: both must be under-threshold to pass.
    decorators = [limiter.limit('3 per hour; 10 per day')]

    @ns_mail.expect(mail_model, validate=True)
    @ns_mail.response(200, 'Mail sent successfully')
    @ns_mail.response(400, 'Unable to Send Mail')
    @ns_mail.response(429, 'Too many requests')
    def post(self):
        try:
            data = request.get_json() or {}
            name = (data.get('name') or '').strip()
            sender_mail = (data.get('email') or '').strip()
            message = (data.get('message') or '').strip()

            if not (name and sender_mail and message):
                return error_response(400, "Missing required fields")

            default_sender = app.config.get('MAIL_DEFAULT_SENDER')
            recipient = app.config.get('MAIL_RECIPIENT') or default_sender
            if not default_sender or not recipient:
                app.logger.error(
                    'MAIL_DEFAULT_SENDER or MAIL_RECIPIENT not configured'
                )
                return error_response(400, 'Mail service not configured')

            # Standard contact-form pattern:
            #   From:      "<visitor> via rafin.dev" + verified sender email
            #              (SendGrid rejects unverified From addresses)
            #   Reply-To:  the visitor, so hitting Reply in the inbox replies
            #              to them directly.
            #   Body:      just the message the visitor typed.
            msg = Message(
                subject=f"[rafin.dev] Message from {name}",
                sender=(f"{name} via rafin.dev", default_sender),
                recipients=[recipient],
                reply_to=(name, sender_mail),
                body=message,
            )
            mail.send(msg)
            return {"status": "success", "message": "Mail sent"}, 200
        except Exception as e:
            app.logger.error(f'Mail send failed: {e}')
            return error_response(400, 'Unable to Send Mail')


ns_mail.add_resource(MailResource, '/')
