from flask_restx import fields, Model
from project.server.api.projects import ns_projects

create_project_type = Model('CreateProject', {
    'user_id': fields.String(required=True, description='The user ID'),
    'title': fields.String(required=True, description='The project title'),
    'description': fields.String(description='The project description'),
    'year': fields.String(description='Year or date range, e.g. "2024" or "Jan 2024 - Present"'),
    'tech_stack': fields.List(fields.String, description='List of technologies used'),
    'github_link': fields.String(description='Link to the GitHub repository'),
    'live_link': fields.String(description='Link to the live project'),
    'thumbnail_url': fields.String(description='URL of the project thumbnail'),
})

update_project_type = Model('UpdateProject', {
    'title': fields.String(description='The project title'),
    'description': fields.String(description='The project description'),
    'year': fields.String(description='Year or date range'),
    'tech_stack': fields.List(fields.String, description='List of technologies used'),
    'github_link': fields.String(description='Link to the GitHub repository'),
    'live_link': fields.String(description='Link to the live project'),
    'thumbnail_url': fields.String(description='URL of the project thumbnail'),
})

create_project_model = ns_projects.add_model('CreateProject', create_project_type)
update_project_model = ns_projects.add_model('UpdateProject', update_project_type)
