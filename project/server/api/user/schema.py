from flask_restx import fields, Model
from project.server.api.user import ns_user

create_user_type = Model('CreateUser', {
    'username': fields.String(required=True, description='The username of the user'),
    'full_name': fields.String(required=True, description='The full name of the user'),
    'designation': fields.String(required=True, description='The designation of the user'),
    'about': fields.String(description='Information about the user'),
    'cv_link': fields.String(description='Link to the user\'s CV'),
    'profile_picture_link': fields.String(description='Link to the user\'s profile picture'),
    'skills': fields.List(fields.Nested({
        'skill': fields.String(required=True, description='The name of the skill'),
        'icon_link': fields.String(required=True, description='The link to the skill icon')
    }), description='A list of skills associated with the user')
})

update_user_type = Model('UpdateUser', {
    'username': fields.String(description='The username of the user'),
    'full_name': fields.String(description='The full name of the user'),
    'designation': fields.String(description='The designation of the user'),
    'about': fields.String(description='Information about the user'),
    'cv_link': fields.String(description='Link to the user\'s CV'),
    'profile_picture_link': fields.String(description='Link to the user\'s profile picture'),
    'skills': fields.List(fields.Nested({
        'skill': fields.String(required=True, description='The name of the skill'),
        'icon_link': fields.String(required=True, description='The link to the skill icon')
    }), description='A list of skills associated with the user')
})

create_user_model = ns_user.add_model('CreateUser', create_user_type)
update_user_model = ns_user.add_model('UpdateUser', update_user_type)
