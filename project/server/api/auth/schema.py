from flask_restx import fields
from project.server.api.auth import ns_auth

login_model = ns_auth.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})
