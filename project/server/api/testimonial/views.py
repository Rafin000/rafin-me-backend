from flask import request, current_app as app
from flask_restx import Resource
from project.server.models.models import Testimonials
from project.server.api.testimonial.schema import *
from project.server.api.testimonial import ns_testimonial
from project.server import db
from project.server.utils import error_response

class TestimonialList(Resource):
    @ns_testimonial.expect(create_testimonial_model, validate=True)
    @ns_testimonial.response(201, "Successfully Created Testimonial")
    @ns_testimonial.response(400, "Unable to Create Testimonial")
    def post(self):
        try:
            data = request.get_json()
            new_testimonial = Testimonials(
                user_id=data['user_id'],
                name=data['name'],
                content=data['content'],
                designation=data.get('designation'),
                company=data.get('company')
            )
            db.session.add(new_testimonial)
            db.session.commit()
            return {"message": "Successfully Created Testimonial"}, 201
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Create Testimonial")

    @ns_testimonial.response(200, "Successfully Retrieved Testimonials")
    @ns_testimonial.response(400, "Unable to Retrieve Testimonials")
    def get(self):
        try:
            testimonials = Testimonials.query.all()
            serialized_testimonials = [
                {
                    'id': str(testimonial.id),
                    'user_id': str(testimonial.user_id),
                    'name': testimonial.name,
                    'content': testimonial.content,
                    'designation': testimonial.designation,
                    'company': testimonial.company
                } for testimonial in testimonials
            ]
            return {"message": "Successfully Retrieved Testimonials", "data": serialized_testimonials}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Testimonials")

class Testimonial(Resource):
    @ns_testimonial.response(200, "Successfully Retrieved Testimonial")
    @ns_testimonial.response(400, "Unable to Retrieve Testimonial")
    def get(self, testimonial_id):
        try:
            testimonial = Testimonials.query.filter_by(id=testimonial_id).first()
            if not testimonial:
                return error_response(400, "Testimonial not found")

            serialized_testimonial = {
                'id': str(testimonial.id),
                'user_id': str(testimonial.user_id),
                'name': testimonial.name,
                'content': testimonial.content,
                'designation': testimonial.designation,
                'company': testimonial.company
            }
            return {"message": "Successfully Retrieved Testimonial", "data": serialized_testimonial}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Testimonial")

    @ns_testimonial.expect(update_testimonial_model, validate=True)
    @ns_testimonial.response(200, "Successfully Updated Testimonial")
    @ns_testimonial.response(400, "Unable to Update Testimonial")
    def put(self, testimonial_id):
        try:
            data = request.get_json()
            testimonial = Testimonials.query.filter_by(id=testimonial_id).first()

            if not testimonial:
                return error_response(400, "Testimonial not found")

            testimonial.name = data.get('name', testimonial.name)
            testimonial.content = data.get('content', testimonial.content)
            testimonial.designation = data.get('designation', testimonial.designation)
            testimonial.company = data.get('company', testimonial.company)
            
            db.session.commit()
            return {"message": "Successfully Updated Testimonial"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Update Testimonial")

    @ns_testimonial.response(200, "Successfully Deleted Testimonial")
    @ns_testimonial.response(400, "Unable to Delete Testimonial")
    def delete(self, testimonial_id):
        try:
            testimonial = Testimonials.query.filter_by(id=testimonial_id).first()
            if not testimonial:
                return error_response(400, "Testimonial not found")

            db.session.delete(testimonial)
            db.session.commit()
            return {"message": "Successfully Deleted Testimonial"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Delete Testimonial")

ns_testimonial.add_resource(TestimonialList, '/')
ns_testimonial.add_resource(Testimonial, '/<string:testimonial_id>')
