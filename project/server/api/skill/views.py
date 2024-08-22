from flask import request, current_app as app
from flask_restx import Resource
from project.server.models.models import Users, UserSkills
from project.server import db
from project.server.api.skill import ns_user_skill
from project.server.utils import error_response

class UserSkillsListResource(Resource):
    @ns_user_skill.response(200, "Successfully Added Skill")
    @ns_user_skill.response(400, "Unable to Add Skill")
    def post(self):
        try:
            data = request.get_json()
            skill = data.get('skill')
            icon_link = data.get('icon_link')
            user_id = data.get('user_id')

            if not skill or not icon_link:
                return error_response(400, "Skill and icon_link are required")

            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(404, "User not found")

            new_skill = UserSkills(user_id=user_id, skill=skill, icon_link=icon_link)
            db.session.add(new_skill)
            db.session.commit()

            return {"message": "Successfully Added Skill", "user_id": str(user_id)}, 200

        except Exception as e:
            app.logger.error(f"Error adding skill for user_id {user_id}: {e}")
            return error_response(400, 'Unable to Add Skill')

    @ns_user_skill.response(200, "Successfully Retrieved Skills")
    @ns_user_skill.response(400, "Unable to Retrieve Skills")
    def get(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(404, "User not found")

            skills = UserSkills.query.filter_by(user_id=user_id).all()
            skills_list = [
                {
                    'id': str(skill.id),
                    'skill': skill.skill,
                    'icon_link': skill.icon_link,
                    'user_id': str(skill.user_id)
                }
                for skill in skills
            ]

            return skills_list, 200

        except Exception as e:
            app.logger.error(f"Error retrieving skills for user_id {user_id}: {e}")
            return error_response(400, "Unable to Retrieve Skills")

class UserSkillsResource(Resource):
    @ns_user_skill.response(200, "Successfully Deleted Skill")
    @ns_user_skill.response(400, "Unable to Delete Skill")
    def delete(self, skill_id):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(404, "User not found")

            skill_to_delete = UserSkills.query.filter_by(id=skill_id, user_id=user_id).first()
            if not skill_to_delete:
                return error_response(404, "Skill not found")

            db.session.delete(skill_to_delete)
            db.session.commit()

            return {"message": "Successfully Deleted Skill"}, 200

        except Exception as e:
            app.logger.error(f"Error deleting skill for user_id {user_id}: {e}")
            return error_response(400, "Unable to Delete Skill")

    @ns_user_skill.response(200, "Successfully Updated Skill")
    @ns_user_skill.response(400, "Unable to Update Skill")
    def put(self, skill_id):
        try:
            data = request.get_json()
            skill = data.get('skill')
            icon_link = data.get('icon_link')
            user_id = data.get('user_id')

            if not skill and not icon_link:
                return error_response(400, "Skill and icon_link are required")

            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(404, "User not found")

            skill_to_update = UserSkills.query.filter_by(id=skill_id, user_id=user_id).first()
            if not skill_to_update:
                return error_response(404, "Skill not found")

            skill_to_update.skill = skill or skill_to_update.skill
            skill_to_update.icon_link = icon_link or skill_to_update.icon_link
            db.session.commit()

            return {"message": "Successfully Updated Skill"}, 200

        except Exception as e:
            app.logger.error(f"Error updating skill for user_id {user_id}, skill_id {skill_id}: {e}")
            return error_response(400, "Unable to Update Skill")

ns_user_skill.add_resource(UserSkillsListResource, '/', endpoint='user-skills-list')
ns_user_skill.add_resource(UserSkillsResource, '/<string:skill_id>', endpoint='user-skills')
