from flask import copy_current_request_context, request
from flask import current_app as app
from flask_restx import Resource
from project.server.api.mail.schema import mail_model
from project.server.api.mail import ns_mail
from project.server.utils import error_response
from flask_mail import Message
from project.server import mail

class MailResource(Resource):
    @ns_mail.expect(mail_model, validate=True)
    @ns_mail.response(200, 'Mail sent successfully')
    @ns_mail.response(400, 'Unable to Send Mail')
    def post(self):
        try:
            data = request.get_json()
            name = data.get('name')
            sender_mail = data.get('email')
            message = data.get('message')

            if not (name and sender_mail and message):
                return error_response(400, "Missing required fields")

            msg = Message(
                subject=f"Message from {name}",
                sender=sender_mail,
                recipients=['u1704038@student.cuet.ac.bd'],
                body=f"{message}\nMail : {sender_mail}"
            )
            mail.send(msg)
            return {"status": "success", "message": "Mail sent asynchronously!"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Send Mail")
        
ns_mail.add_resource(MailResource, '/')
