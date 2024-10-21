from flask import request, current_app as app
from flask_restx import Resource
from project.server.docorators import check_apikey
from project.server.models.models import Experience
from project.server.api.Experience import ns_experience
from project.server import db
from project.server.utils import error_response

class ExperienceList(Resource):
    @check_apikey
    def post(self):
        try:
            data = request.get_json()
            new_experience = Experience(
                user_id=data['user_id'],
                year=data['year'],
                position=data['position'],
                company=data['company'],
                work_details=data.get('work_details', [])
            )
            db.session.add(new_experience)
            db.session.commit()
            return {"message": "Successfully Created Experience"}, 201
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Create Experience")

    @check_apikey
    def get(self):
        try:
            experience_list = Experience.query.all()
            serialized_experience = [
                {
                    'id': str(experience.id),
                    'user_id': str(experience.user_id),
                    'year': experience.year,
                    'position': experience.position,
                    'company': experience.company,
                    'work_details': experience.work_details
                } for experience in experience_list
            ]
            return {"message": "Successfully Retrieved Experience", "data": serialized_experience}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Experience")


class ExperienceItem(Resource):
    @check_apikey
    def get(self, experience_id):
        try:
            experience = Experience.query.filter_by(id=experience_id).first()
            if not experience:
                return error_response(400, "Experience not found")

            serialized_experience = {
                'id': str(experience.id),
                'user_id': str(experience.user_id),
                'year': experience.year,
                'position': experience.position,
                'company': experience.company,
                'work_details': experience.work_details
            }
            return {"message": "Successfully Retrieved Experience", "data": serialized_experience}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Experience")

    @check_apikey
    def put(self, experience_id):
        try:
            data = request.get_json()
            experience = Experience.query.filter_by(id=experience_id).first()

            if not experience:
                return error_response(400, "Experience not found")

            experience.year = data.get('year', experience.year)
            experience.position = data.get('position', experience.position)
            experience.company = data.get('company', experience.company)
            experience.work_details = data.get('work_details', experience.work_details)

            db.session.commit()
            return {"message": "Successfully Updated Experience"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Update Experience")

    @check_apikey
    def delete(self, experience_id):
        try:
            experience = Experience.query.filter_by(id=experience_id).first()
            if not experience:
                return error_response(400, "Experience not found")

            db.session.delete(experience)
            db.session.commit()
            return {"message": "Successfully Deleted Experience"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Delete Experience")


ns_experience.add_resource(ExperienceList, '/')
ns_experience.add_resource(ExperienceItem, '/<string:experience_id>')