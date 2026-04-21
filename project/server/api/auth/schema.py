from flask_restx import fields
from project.server.api.auth import ns_auth

login_model = ns_auth.model('Login', {
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
})

forgot_password_model = ns_auth.model('ForgotPassword', {
    'email': fields.String(required=True, description='Email'),
})

reset_password_model = ns_auth.model('ResetPassword', {
    'email': fields.String(required=True, description='Email'),
    'code': fields.String(required=True, description='Reset code'),
    'new_password': fields.String(required=True, description='New password'),
})

update_me_model = ns_auth.model('UpdateMe', {
    'email': fields.String(required=False, description='New email'),
    'current_password': fields.String(required=False, description='Current password (required when changing password)'),
    'new_password': fields.String(required=False, description='New password'),
})
