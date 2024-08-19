from flask_restx import fields, Model
from project.server.api.social import ns_social

create_skill_type = Model('CreateSkill', {
    'skill': fields.String(required=True, description='The Skill to add'),
})

create_skill_model = ns_social.add_model('CreateSkill', create_skill_type)