from flask import request, current_app as app
from flask_restx import Resource
from project.server.models.models import Education
from project.server.api.Education import ns_education
from project.server import db
from project.server.utils import error_response

class EducationList(Resource):
    def post(self):
        try:
            data = request.get_json()
            new_education = Education(
                user_id=data['user_id'],
                year=data['year'],
                degree=data['degree'],
                university=data['university'],
                cgpa=data.get('cgpa')
            )
            db.session.add(new_education)
            db.session.commit()
            return {"message": "Successfully Created Education"}, 201
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Create Education")

    def get(self):
        try:
            education_list = Education.query.all()
            serialized_education = [
                {
                    'id': str(education.id),
                    'user_id': str(education.user_id),
                    'year': education.year,
                    'degree': education.degree,
                    'university': education.university,
                    'cgpa': education.cgpa
                } for education in education_list
            ]
            return {"message": "Successfully Retrieved Education", "data": serialized_education}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Education")


class EducationItem(Resource):
    def get(self, education_id):
        try:
            education = Education.query.filter_by(id=education_id).first()
            if not education:
                return error_response(400, "Education not found")

            serialized_education = {
                'id': str(education.id),
                'user_id': str(education.user_id),
                'year': education.year,
                'degree': education.degree,
                'university': education.university,
                'cgpa': education.cgpa
            }
            return {"message": "Successfully Retrieved Education", "data": serialized_education}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Education")

    def put(self, education_id):
        try:
            data = request.get_json()
            education = Education.query.filter_by(id=education_id).first()

            if not education:
                return error_response(400, "Education not found")

            education.year = data.get('year', education.year)
            education.degree = data.get('degree', education.degree)
            education.university = data.get('university', education.university)
            education.cgpa = data.get('cgpa', education.cgpa)

            db.session.commit()
            return {"message": "Successfully Updated Education"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Update Education")

    def delete(self, education_id):
        try:
            education = Education.query.filter_by(id=education_id).first()
            if not education:
                return error_response(400, "Education not found")

            db.session.delete(education)
            db.session.commit()
            return {"message": "Successfully Deleted Education"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Delete Education")


ns_education.add_resource(EducationList, '/')
ns_education.add_resource(EducationItem, '/<string:education_id>')