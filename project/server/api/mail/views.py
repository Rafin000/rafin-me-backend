from flask import request
from flask import current_app as app
from flask_restx import Resource
from flask_mail import Message

from project.server import mail
from project.server.api.mail import ns_mail
from project.server.api.mail.schema import mail_model
from project.server.utils import error_response


class MailResource(Resource):
    @ns_mail.expect(mail_model, validate=True)
    @ns_mail.response(200, 'Mail sent successfully')
    @ns_mail.response(400, 'Unable to Send Mail')
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

            body = (
                f"You received a new message from rafin.dev contact form.\n\n"
                f"From: {name} <{sender_mail}>\n"
                f"---\n"
                f"{message}\n"
            )

            msg = Message(
                subject=f"[rafin.dev] Message from {name}",
                sender=default_sender,      # must be a verified sender at the provider
                recipients=[recipient],
                reply_to=sender_mail,       # so "Reply" goes back to the visitor
                body=body,
            )
            mail.send(msg)
            return {"status": "success", "message": "Mail sent"}, 200
        except Exception as e:
            app.logger.error(f'Mail send failed: {e}')
            return error_response(400, 'Unable to Send Mail')


ns_mail.add_resource(MailResource, '/')
