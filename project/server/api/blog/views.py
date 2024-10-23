from flask import current_app as app, request
from flask_restx import Resource
from project.server.api.blog import ns_blog
from project.server.docorators import check_apikey
from project.server.models.models import Blogs
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

class BlogList(Resource):
    @check_apikey
    @ns_blog.expect(create_blog_model, validate=True)
    @ns_blog.response(200, "Successfully Created Blog")
    @ns_blog.response(400, "Unable to Create Blog")
    def post(self):
        try:
            data = request.get_json()
            title = data.get('title')
            summary = data.get('summary')
            reading_time = data.get('reading_time')
            thumbnail_url = data.get('thumbnail_url')
            tags = data.get('tags', [])
            content = data.get('content')
            author = data.get('author')

            blog = Blogs(
                title=title, 
                content=content, 
                author=author,
                summary=summary,
                reading_time=reading_time,
                thumbnail_url=thumbnail_url,
                tags=tags
            )
            
            db.session.add(blog)
            db.session.commit()

            return {
                "message" : "Successfully Created Blog"
            }, 200
        except Exception as e:
            app.logger.info(e)
            return error_response(400, "Unable to Create Blog")
        

    @check_apikey
    @ns_blog.response(200, "Successfully Retrieved Blogs")
    @ns_blog.response(400, "Unable to retrieve blogs")
    def get(self):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            blogs = Blogs.query.order_by(Blogs.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
            serialized_blogs = []
            for blog in blogs.items:
                serialized_blogs.append({
                    'id': str(blog.id),
                    'title': blog.title,
                    'summary': blog.summary,
                    'reading_time': blog.reading_time,
                    'thumbnail_url': blog.thumbnail_url,
                    'tags': blog.tags,
                    'content': blog.content,
                    'author': blog.author,
                    'likes': blog.likes,
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


class Blog(Resource):   
    @check_apikey             
    @ns_blog.response(200, "Successfully Retrieved Blog")
    @ns_blog.response(400, "Unable to Retrieve Blog")
    def get(self, blog_id):
        try:
            blog = Blogs.query.filter_by(id=blog_id).first()

            if not blog:
                return error_response(400, "Blog not found")

            serialized_blog = {
                'id': str(blog.id),
                'title': blog.title,
                'summary': blog.summary,
                'reading_time': blog.reading_time,
                'thumbnail_url': blog.thumbnail_url,
                'tags': blog.tags,
                'content': blog.content,
                'author': blog.author,
                'likes': blog.likes,
                'created_at': blog.created_at.timestamp(),
                'updated_at': blog.updated_at.timestamp()
            }

            return {
                'message': "Successfully Retrieved Blog",
                'data': serialized_blog
            }, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Blog")
        
    @check_apikey
    @ns_blog.expect(update_blog_model, validate=True)
    @ns_blog.response(200, "Successfully Updated Blog")
    @ns_blog.response(400, "Unable to Update Blog")
    def put(self, blog_id):
        try:
            data = request.get_json()
            blog = Blogs.query.filter_by(id=blog_id).first()

            if not blog:
                return error_response(400, "Blog not found")

            blog.title = data.get('title', blog.title)
            blog.summary = data.get('summary', blog.summary)
            blog.reading_time = data.get('reading_time', blog.reading_time)
            blog.thumbnail_url = data.get('thumbnail_url', blog.thumbnail_url)
            blog.tags = data.get('tags', blog.tags)
            blog.content = data.get('content', blog.content)
            blog.author = data.get('author', blog.author)
            
            db.session.commit()

            return {
                "message": "Successfully Updated Blog"
            }, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Update Blog")


    @check_apikey
    @ns_blog.response(200, "Successfully Deleted Blog")
    @ns_blog.response(400, "Unable to Delete Blog")
    def delete(self, blog_id):
        try:
            blog = Blogs.query.filter_by(id=blog_id).first()

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

class BlogLike(Resource):   
    @check_apikey
    @ns_blog.response(200, "Successfully Liked Blog")
    @ns_blog.response(400, "Unable to Like Blog")
    def post(self, blog_id):
        try:
            blog = Blogs.query.filter_by(id=blog_id).first()

            if not blog:
                return error_response(400, "Blog not found")

            blog.likes += 1
            db.session.commit()

            return {
                "message": "Successfully Liked Blog",
                "likes": blog.likes
            }, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Like Blog")
        
        
ns_blog.add_resource(Alive, "/alive", endpoint="alive-blog-view")
ns_blog.add_resource(BlogList, "/",  endpoint="blog-list")
ns_blog.add_resource(Blog, "/<string:blog_id>",  endpoint="blog")
ns_blog.add_resource(BlogLike, "/<string:blog_id>/like",  endpoint="blog-like")