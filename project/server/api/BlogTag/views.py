from flask_restx import Namespace, Resource
from flask import request
from flask import current_app as app
from project.server import db
from project.server.docorators import check_apikey
from project.server.models.models import Blogs
from project.server.utils import error_response

ns_blog_tags = Namespace('blog-tags', description='Blog Tag Operations')

class BlogTag(Resource):
    @check_apikey
    @ns_blog_tags.response(200, "Successfully Retrieved Tags")
    @ns_blog_tags.response(400, "Unable to Retrieve Tags")
    def get(self, blog_id):
        try:
            blog = Blogs.query.filter_by(id=blog_id).first()
            if not blog:
                return error_response(400, "Blog not found")

            return {
                "tags": blog.tags
            }, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Tags")

    @check_apikey
    @ns_blog_tags.response(200, "Successfully Added Tag")
    @ns_blog_tags.response(400, "Unable to Add Tag")
    def post(self, blog_id):
        try:
            data = request.get_json()
            tag = data.get('tag')
            
            if not tag:
                return error_response(400, "Tag is required")

            blog = Blogs.query.filter_by(id=blog_id).first()
            if not blog:
                return error_response(400, "Blog not found")

            if tag not in blog.tags:
                blog.tags.append(tag)
                db.session.commit()
                return {"message": "Successfully Added Tag"}, 200
            else:
                return error_response(400, "Tag already exists")

        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Add Tag")

    @check_apikey
    @ns_blog_tags.response(200, "Successfully Deleted Tag")
    @ns_blog_tags.response(400, "Unable to Delete Tag")
    def delete(self, blog_id):
        try:
            data = request.get_json()
            tag = data.get('tag')

            if not tag:
                return error_response(400, "Tag is required")

            blog = Blogs.query.filter_by(id=blog_id).first()
            if not blog:
                return error_response(400, "Blog not found")

            if tag in blog.tags:
                blog.tags = [t for t in blog.tags if t != tag]
                db.session.commit()
                return {"message": "Successfully Deleted Tag"}, 200
            else:
                return error_response(400, "Tag not found")

        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Delete Tag")

ns_blog_tags.add_resource(BlogTag, "/<string:blog_id>/tag", endpoint="blog-tag")
