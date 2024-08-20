from flask_restx import fields
from project.server.api.mail import ns_mail

mail_type = ns_mail.model('Mail', {
    'name': fields.String(required=True, description='Sender Name'),
    'email': fields.String(required=True, description='Sender Email'),
    'message': fields.String(required=True, description='Email Content'),
})

mail_model = ns_mail.add_model('Mail', mail_type)