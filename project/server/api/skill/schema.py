from flask_restx import fields, Model
from project.server.api.skill import ns_user_skill

create_skill_type = Model('CreateSkill', {
    'skill': fields.String(required=True, description='The name of the skill'),
    'icon_link': fields.String(required=True, description='The link to the skill icon')
})

create_skill_model = ns_user_skill.add_model('CreateSkill', create_skill_type)
