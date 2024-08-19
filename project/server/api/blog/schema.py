from flask_restx import Model, fields
from project.server.api.blog import ns_blog

create_blog_type = Model('CreateBlog',{
    'title': fields.String(required=True, description='Blog Title'),
    'summary': fields.String(description='Blog Summary'),
    'reading_time': fields.Integer(description='Reading Time in Minutes'),
    'thumbnail_url': fields.String(description='Thumbnail Image URL'),
    'tags': fields.List(fields.String, description='List of Tags'),
    'content': fields.String(required=True, description='Blog Content'),
    'author': fields.String(required=True, description='Author Name'),
})

update_blog_type = Model('UpdateBlog',{
    'blog_id': fields.String(required=True, description='Blog ID'),
    'title': fields.String(description='Blog Title'),
    'summary': fields.String(description='Blog Summary'),
    'reading_time': fields.Integer(description='Reading Time in Minutes'),
    'thumbnail_url': fields.String(description='Thumbnail Image URL'),
    'tags': fields.List(fields.String, description='List of Tags'),
    'content': fields.String(description='Blog Content'),
    'author': fields.String(description='Author Name'),
})


create_blog_model = ns_blog.add_model('CreateBlog', create_blog_type)
update_blog_model = ns_blog.add_model('UpdateBlog', update_blog_type)