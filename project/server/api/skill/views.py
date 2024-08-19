from flask import request
from flask import current_app as app
from flask_restx import Resource
from project.server.models.models import Users
from project.server.api.skill.schema import *
from project.server.api.skill import ns_user_skill
from project.server import db
from project.server.utils import error_response

class UserSkillResource(Resource):
    @ns_user_skill.expect(create_skill_model, validate=True)
    @ns_user_skill.response(201, 'Skill successfully added')
    @ns_user_skill.response(400, 'Validation Error')
    @ns_user_skill.response(500, 'Internal Server Error')
    def post(self, user_id):
        try:
            data = request.get_json()
            skill = data.get('skill')

            if not skill:
                return error_response(400, 'Skill is required')

            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(404, 'User not found')
            print(user.skills)
            if user.skills:
                if skill in user.skills:
                    return error_response(400, 'Skill already exists')
                user.skills = list(set(user.skills + [skill]))
            else:
                user.skills = [skill]

            db.session.commit()
            return {'message': 'Skill added successfully'}, 201
        except Exception as e:
            app.logger.error(f"Error adding skill for user ID {user_id}: {e}")
            return error_response(500, 'Internal Server Error')


    @ns_user_skill.response(200, 'Skill successfully deleted')
    @ns_user_skill.response(404, 'User or skill not found')
    @ns_user_skill.response(500, 'Internal Server Error')
    def delete(self, user_id):
        try:
            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(404, 'User not found')
            data = request.get_json()
            skill = data.get('skill')

            if not skill:
                return error_response(400, 'Skill is required')
            
            if user.skills and skill in user.skills:
                user.skills = [s for s in user.skills if s != skill]
                db.session.commit()
                return {'message': 'Skill deleted successfully'}, 200
            else:
                return error_response(404, 'Skill not found')
        except Exception as e:
            app.logger.error(f"Error deleting skill for user ID {user_id}: {e}")
            return error_response(500, 'Internal Server Error')

ns_user_skill.add_resource(UserSkillResource, '/<string:user_id>')
