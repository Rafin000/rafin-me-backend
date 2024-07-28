from flask_restx import Api
from project.server.api.blog.views import ns_blog

api_blog = Api(version='1.0', title='Blog Service API', prefix='/api/v1')
api_blog.add_namespace(ns_blog, path='/blog-service')