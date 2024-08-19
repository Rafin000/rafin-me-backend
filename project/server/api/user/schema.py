from flask_restx import fields, Model
from project.server.api.user import ns_user

create_user_type = Model('CreateUser', {
    'username': fields.String(required=True, description='The username of the user'),
    'full_name': fields.String(required=True, description='The full name of the user'),
    'designation': fields.String(required=True, description='The designation of the user'),
    'about': fields.String(description='Information about the user'),
    'skill': fields.List(fields.String, description='A list of skills associated with the user')
})


create_user_type = Model('UpdateUser', {
    'username': fields.String(description='The username of the user'),
    'full_name': fields.String(description='The full name of the user'),
    'designation': fields.String(description='The designation of the user'),
    'about': fields.String(description='Information about the user'),
    'skill': fields.List(fields.String, description='A list of skills associated with the user')
})


create_user_model = ns_user.add_model('CreateUser', create_user_type)
update_user_model = ns_user.add_model('UpdateUser', create_user_type)