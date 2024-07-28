from flask_restx import Model, fields
from project.server.api.blog import ns_blog

create_blog_type = Model('CreateBlog',{
    'title': fields.String(required=True, description='Blog Title'),
    'content': fields.String(required=True, description='Blog Content'),
    'author': fields.String(required=True, description='Author Name'),
})

update_blog_type = Model('UpdateBlog',{
    'blog_id': fields.String(required=True, description='Blog Id'),
    'title': fields.String(description='Blog Title'),
    'content': fields.String(description='Blog Content'),
    'author': fields.String(description='Author Name'),
})

delete_blog_type = Model('DeleteBlog',{
    'blog_id': fields.String(required=True, description='Blog Id')
})

create_blog_model = ns_blog.add_model('CreateBlog', create_blog_type)
update_blog_model = ns_blog.add_model('UpdateBlog', update_blog_type)
delete_blog_model = ns_blog.add_model('DeleteBlog', delete_blog_type)