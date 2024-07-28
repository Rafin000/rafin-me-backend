from flask import current_app as app, request
import requests
from flask_restx import Resource
from project.server.api.blog import ns_blog
from project.server.models.blog import Blog
from project.server.api.blog.schema import *
from project.server import db
from project.server.utils import error_response


class Alive(Resource):
    """
    * Method: GET
    * Check if the API is running
    * Tested with postman
    """
    def get(self):
        response_object = {
            'status': 'success',
            'message': "Alive",
        }
        return response_object, 200
    

class BlogPost(Resource):
    @ns_blog.expect(create_blog_model, validate=True)
    @ns_blog.response(200, "Successfully Created Blog")
    @ns_blog.response(400, "Unable to Create Blog")
    def post(self):
        try:
            data = request.get_json()
            title = data.get('title')
            content = data.get('content')
            author = data.get('author')

            blog = Blog(
                title = title, 
                content = content, 
                author = author
                )
            
            db.session.add(blog)
            db.session.commit()

            return {
                "message" : "Successfully Created Blog"
            }, 200
        except Exception as e:
            app.logger.info(e)
            return error_response(400, "Unable to Create Blog")
        
    @ns_blog.response(200, "Successfully Retrieved Blogs")
    @ns_blog.response(400, "Unable to retrieve blogs")
    # def get(self):
    #     try:
    #         blogs = Blog.query.order_by(Blog.created_at.desc()).all()
    #         serialized_blogs = []
    #         for blog in blogs:
    #             serialized_blogs.append({
    #                 'id': str(blog.id),
    #                 'title': blog.title,
    #                 'content': blog.content,
    #                 'author': blog.author,
    #                 'created_at': blog.created_at.timestamp(),
    #                 'updated_at': blog.updated_at.timestamp()
    #             })
    #         app.logger.info(serialized_blogs)
    #         return {
    #             'message' : "Successfully Retrieved Blogs",
    #             'data' : serialized_blogs
    #         }, 200
    #     except Exception as e:
    #         app.logger.error(e)
    #         return error_response(400, "Unable to retrieve blogs")
    def get(self):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            blogs = Blog.query.order_by(Blog.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
            serialized_blogs = []
            for blog in blogs.items:
                serialized_blogs.append({
                    'id': str(blog.id),
                    'title': blog.title,
                    'content': blog.content,
                    'author': blog.author,
                    'created_at': blog.created_at.timestamp(),
                    'updated_at': blog.updated_at.timestamp()
                })

            return {
                'message': "Successfully Retrieved Blogs",
                'data': serialized_blogs,
                'total': blogs.total,
                'pages': blogs.pages,
                'current_page': blogs.page
            }, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to retrieve blogs")
        
        
    @ns_blog.expect(update_blog_model, validate=True)
    @ns_blog.response(200, "Successfully Updated Blog")
    @ns_blog.response(400, "Unable to Update Blog")
    def put(self):
        try:
            data = request.get_json()
            blog_id = data.get('blog_id')
            blog = Blog.query.filter_by(id=blog_id).first()

            if not blog:
                return error_response(400, "Blog not found")

            blog.title = data.get('title', blog.title)
            blog.content = data.get('content', blog.content)
            blog.author = data.get('author', blog.author)
            
            db.session.commit()

            return {
                "message": "Successfully Updated Blog"
            }, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Update Blog")


    @ns_blog.expect(delete_blog_model, validate=True)
    @ns_blog.response(200, "Successfully Deleted Blog")
    @ns_blog.response(400, "Unable to Delete Blog")
    def delete(self):
        try:
            data = request.get_json()
            blog_id = data.get('blog_id')
            blog = Blog.query.filter_by(id=blog_id).first()

            if not blog:
                return error_response(400, "Blog not found")

            db.session.delete(blog)
            db.session.commit()

            return {
                "message": "Successfully Deleted Blog"
            }, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Delete Blog")

ns_blog.add_resource(Alive, "/alive", endpoint="alive-blog-view")
ns_blog.add_resource(BlogPost, "/blog",  endpoint="blog")