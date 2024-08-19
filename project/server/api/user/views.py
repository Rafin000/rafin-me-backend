from flask import request, current_app as app
from flask_restx import Resource
from project.server.models.models import Users
from project.server.api.user.schema import *
from project.server.api.user import ns_user
from project.server import db
from project.server.utils import error_response

class UserList(Resource):
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
                skills=data.get('skills')
            )
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Successfully Created User"}, 201
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Create User")

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
                    'skills': user.skills
                } for user in users
            ]
            return {"message": "Successfully Retrieved Users", "data": serialized_users}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Users")

class User(Resource):
    @ns_user.response(200, "Successfully Retrieved User")
    @ns_user.response(400, "Unable to Retrieve User")
    def get(self, user_id):
        try:
            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(400, "User not found")

            # Serialize user data
            serialized_user = {
                'id': str(user.id),
                'username': user.username,
                'full_name': user.full_name,
                'designation': user.designation,
                'about': user.about,
                'skills': user.skills,
                'testimonials': [
                    {
                        'id': str(testimonial.id),
                        'name': testimonial.name,
                        'date': testimonial.date.isoformat(),
                        'designation': testimonial.designation,
                        'content': testimonial.content,
                        'company' : testimonial.company
                    } for testimonial in user.testimonials
                ],
                'social_media_links': {
                    'facebook': user.social_media_links[0].facebook if user.social_media_links else None,
                    'linkedin': user.social_media_links[0].linkedin if user.social_media_links else None,
                    'instagram': user.social_media_links[0].instagram if user.social_media_links else None,
                    'github': user.social_media_links[0].github if user.social_media_links else None
                }
            }
            return {"message": "Successfully Retrieved User", "data": serialized_user}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve User")

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
            new_skills = data.get('skills', [])
            
            if not isinstance(new_skills, list):
                return error_response(400, "Skills should be a list")

            if user.skills:
                existing_skills = set(user.skills)
            else:
                existing_skills = set()

            for skill in new_skills:
                if skill not in existing_skills:
                    existing_skills.add(skill)

            user.skills = list(existing_skills)
            
            db.session.commit()

            return {"message": "Successfully Updated User"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Update User")


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


# class UserSkill(Resource):
#     # @ns_user.expect(create_skill_model, validate=True)
#     @ns_user.response(201, 'Skill successfully added')
#     @ns_user.response(400, 'Validation Error')
#     @ns_user.response(500, 'Internal Server Error')
#     def post(self, user_id):
#         try:
#             data = request.get_json()
#             skill = data.get('skill')

#             if not skill:
#                 app.logger.warning(f"Post request failed: 'skill' is required for user ID {user_id}")
#                 return error_response(400, 'Skill is required')

#             app.logger.info(f"Attempting to add skill '{skill}' for user ID {user_id}")

#             user = Users.query.filter_by(id=user_id).first()
#             if not user:
#                 app.logger.warning(f"User with ID {user_id} not found")
#                 return error_response(404, 'User not found')

#             if user.skills:
#                 if skill in user.skills:
#                     app.logger.warning(f"Skill '{skill}' already exists for user ID {user_id}")
#                     return error_response(400, 'Skill already exists')
#                 user.skills.append(skill)
#             else:
#                 user.skills = [skill]

#             db.session.commit()
#             app.logger.info(f"Skill '{skill}' added successfully for user ID {user_id}")
#             return {'message': 'Skill added successfully'}, 201
#         except Exception as e:
#             app.logger.error(f"Error adding skill for user ID {user_id}: {e}")
#             return error_response(500, 'Internal Server Error')
        
ns_user.add_resource(UserList, '/')
ns_user.add_resource(User, '/<string:user_id>')
# ns_user.add_resource(UserSkill, '/<string:user_id>/skills')
