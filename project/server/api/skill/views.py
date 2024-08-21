from flask import request
from flask import current_app as app
from flask_restx import Resource
from sqlalchemy.dialects.postgresql import JSONB
from project.server.models.models import Users
from project.server.api.skill.schema import *
from project.server.api.skill import ns_user_skill
from project.server import db
from project.server.utils import error_response

class UserSkillResource(Resource):
    # @ns_user_skill.expect(create_skill_model, validate=True)
    @ns_user_skill.response(201, 'Skill successfully added')
    @ns_user_skill.response(400, 'Validation Error')
    @ns_user_skill.response(404, 'User not found')
    @ns_user_skill.response(500, 'Internal Server Error')
    def post(self, user_id):
        try:
            data = request.get_json()
            skill_name = data.get('skill')
            icon_link = data.get('icon_link')

            if not skill_name or not icon_link:
                return error_response(400, 'Both skill and icon_link are required')

            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(404, 'User not found')

            if user.skills is None:
                user.skills = []

            existing_skills = {s.get('skill') for s in user.skills}
            if skill_name in existing_skills:
                return error_response(400, 'Skill already exists')

            user.skills.append({
                'skill': skill_name,
                'icon_link': icon_link
            })

            app.logger.info(f"Adding skill to user ID {user_id}")

            db.session.commit()

            return {'message': 'Skill added successfully'}, 201
        except Exception as e:
            app.logger.error(f"Error adding skill for user ID {user_id}: {e}")
            return error_response(500, 'Internal Server Error')
    
    # def post(self, user_id):
    #     try:
    #         data = request.get_json()
    #         skill = data.get('skill')
    #         icon_link = data.get('icon_link')

    #         if not skill or not icon_link:
    #             return error_response(400, 'skill and icon_link are required')

    #         user = Users.query.filter_by(id=user_id).first()
    #         if not user:
    #             return error_response(404, 'User not found')

    #         # if user.skills is None:
    #         #     user.skills = []

    #         existing_skills = {s['skill'] for s in user.skills}
    #         if skill in existing_skills:
    #             return error_response(400, 'Skill already exists')

    #         user.skills.append(skill)
    #         app.logger.info(f"Adding skill to user ID {user_id}")

    #         db.session.commit()

    #         return {'message': 'Skill added successfully'}, 201
    #     except Exception as e:
    #         app.logger.error(f"Error adding skill for user ID {user_id}: {e}")
    #         return error_response(500, 'Internal Server Error')


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
            
            if user.skills:
                skills_to_keep = [s for s in user.skills if s['skill'] != skill]
                if len(skills_to_keep) == len(user.skills):
                    return error_response(404, 'Skill not found')
                user.skills = skills_to_keep
                db.session.commit()
                return {'message': 'Skill deleted successfully'}, 200
            else:
                return error_response(404, 'No skills found for the user')
            
        except Exception as e:
            app.logger.error(f"Error deleting skill for user ID {user_id}: {e}")
            return error_response(500, 'Internal Server Error')

ns_user_skill.add_resource(UserSkillResource, '/<string:user_id>/skills')
