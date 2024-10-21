from flask import request, current_app as app
from flask_restx import Resource
from project.server.docorators import check_apikey
from project.server.models.models import Users
from project.server.api.user.schema import *
from project.server.api.user import ns_user
from project.server import db
from project.server.utils import error_response

class UserList(Resource):
    @check_apikey
    @ns_user.expect(create_user_model, validate=True)
    @ns_user.response(201, "Successfully Created User")
    @ns_user.response(400, "Unable to Create User")
    def post(self):
        try:
            data = request.get_json()
            new_user = Users(
                username=data['username'],
                full_name=data['full_name'],
                designation=data['designation'],
                about=data.get('about'),
                cv_link=data.get('cv_link'),
                profile_picture_link=data.get('profile_picture_link'),
                skills=data.get('skills')
            )
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Successfully Created User"}, 201
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Create User")

    @check_apikey
    @ns_user.response(200, "Successfully Retrieved Users")
    @ns_user.response(400, "Unable to Retrieve Users")
    def get(self):
        try:
            users = Users.query.all()
            serialized_users = [
                {
                    'id': str(user.id), 
                    'username': user.username,
                    'full_name': user.full_name,
                    'designation': user.designation,
                    'about': user.about,
                    'cv_link': user.cv_link,
                    'profile_picture_link': user.profile_picture_link,
                    'skills': user.skills
                } for user in users
            ]
            return {"message": "Successfully Retrieved Users", "data": serialized_users}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Users")

class User(Resource):
    @check_apikey
    @ns_user.response(200, "Successfully Retrieved User")
    @ns_user.response(400, "Unable to Retrieve User")
    def get(self, user_id):
        try:
            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(400, "User not found")

            serialized_user = {
                'id': str(user.id), 
                'username': user.username,
                'full_name': user.full_name,
                'designation': user.designation,
                'about': user.about,
                'cv_link': user.cv_link,
                'profile_picture_link': user.profile_picture_link,
                'skills': [
                    {
                        'id': str(skill.id),  
                        'skill': skill.skill,
                        'icon_link': skill.icon_link,
                        'user_id': str(skill.user_id)  
                    } for skill in user.user_skills
                ],
                'testimonials': [
                    {
                        'id': str(testimonial.id),  
                        'name': testimonial.name,
                        'date': testimonial.date.isoformat(),  
                        'designation': testimonial.designation,
                        'content': testimonial.content,
                        'company': testimonial.company,
                        'image_link': testimonial.image_link
                    } for testimonial in user.testimonials
                ],
                'social_media_links': {
                    'facebook': user.social_media_links[0].facebook if user.social_media_links else None,
                    'linkedin': user.social_media_links[0].linkedin if user.social_media_links else None,
                    'instagram': user.social_media_links[0].instagram if user.social_media_links else None,
                    'github': user.social_media_links[0].github if user.social_media_links else None
                },
                'experiences' : [
                    {
                        'id' : str(experience.id),
                        'user_id' : str(experience.user_id),
                        'year' : experience.year,
                        'position' : experience.position,
                        'company' : experience.company,
                        'contributions' : [contribution for contribution in experience.work_details]
                    } for experience in user.experience
                ],
                'education' : [
                    {
                        'id' : str(education.id),
                        'user_id' : str(education.user_id),
                        'year' : education.year,
                        'degree' : education.degree,
                        'university' : education.university,
                        'cgpa' : education.cgpa,
                    } for education in user.education
                ]
            }
            return {"message": "Successfully Retrieved User", "data": serialized_user}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve User")

    @check_apikey
    @ns_user.expect(update_user_model, validate=True)
    @ns_user.response(200, "Successfully Updated User")
    @ns_user.response(400, "Unable to Update User")
    def put(self, user_id):
        try:
            data = request.get_json()
            user = Users.query.filter_by(id=user_id).first()

            if not user:
                return error_response(400, "User not found")

            user.username = data.get('username', user.username)
            user.full_name = data.get('full_name', user.full_name)
            user.designation = data.get('designation', user.designation)
            user.about = data.get('about', user.about)
            user.cv_link = data.get('cv_link', user.cv_link)
            user.profile_picture_link = data.get('profile_picture_link', user.profile_picture_link)
            
            db.session.commit()

            return {"message": "Successfully Updated User"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Update User")

    @check_apikey
    @ns_user.response(200, "Successfully Deleted User")
    @ns_user.response(400, "Unable to Delete User")
    def delete(self, user_id):
        try:
            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(400, "User not found")

            db.session.delete(user)
            db.session.commit()
            return {"message": "Successfully Deleted User"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Delete User")

ns_user.add_resource(UserList, '/')
ns_user.add_resource(User, '/<string:user_id>')
