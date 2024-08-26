from flask_restx import Api
from project.server.api.blog.views import ns_blog
from project.server.api.user.views import ns_user
from project.server.api.social.views import ns_social
from project.server.api.testimonial.views import ns_testimonial
from project.server.api.skill.views import ns_user_skill
from project.server.api.mail.views import ns_mail
from project.server.api.BlogTag.views import ns_blog_tags
from project.server.api.Education.views import ns_education
from project.server.api.Experience.views import ns_experience

api_blog = Api(version='1.0', title='Blog Service API', prefix='/api/v1', doc='/docs')
api_blog.add_namespace(ns_blog, path='/blogs')
api_blog.add_namespace(ns_user, path='/users')
api_blog.add_namespace(ns_social, path='/socials')
api_blog.add_namespace(ns_testimonial, path='/testimonials')
api_blog.add_namespace(ns_user_skill, path='/skills')
api_blog.add_namespace(ns_mail, path='/mails')
api_blog.add_namespace(ns_blog_tags, path='/blogs')
api_blog.add_namespace(ns_education, path='/education')
api_blog.add_namespace(ns_experience, path='/experience')