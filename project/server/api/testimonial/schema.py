from flask_restx import fields, Model
from project.server.api.testimonial import ns_testimonial

create_testimonial_type = Model('CreateTestimonial', {
    'user_id': fields.String(required=True, description='The ID of the user associated with this testimonial'),
    'name': fields.String(required=True, description='The name of the person giving the testimonial'),
    'content': fields.String(required=True, description='The content of the testimonial'),
    'designation': fields.String(description='The designation of the person giving the testimonial'),
    'company': fields.String(description='The Company of that person giving the testimonial'),
    'image_link': fields.String(description='Image of that person giving the testimonial')
})

update_testimonial_type = Model('UpdateTestimonial', {
    'name': fields.String(description='The name of the person giving the testimonial'),
    'content': fields.String(description='The content of the testimonial'),
    'designation': fields.String(description='The designation of the person giving the testimonial'),
    'company': fields.String(description='The Company of that person giving the testimonial'),
    'image_link': fields.String(description='Image of that person giving the testimonial')
})

create_testimonial_model = ns_testimonial.add_model('CreateTestimonial', create_testimonial_type)
update_testimonial_model = ns_testimonial.add_model('UpdateTestimonial', update_testimonial_type)