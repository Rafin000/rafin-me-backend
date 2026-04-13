from flask import request, current_app as app
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from project.server.models.models import Users, Projects
from project.server import db
from project.server.api.projects import ns_projects
from project.server.api.projects.schema import create_project_model, update_project_model
from project.server.utils import error_response, asset_url


def serialize_project(project):
    return {
        'id': str(project.id),
        'user_id': str(project.user_id),
        'title': project.title,
        'description': project.description,
        'year': project.year,
        'contributions': project.contributions or [],
        'tech_stack': project.tech_stack or [],
        'github_link': project.github_link,
        'live_link': project.live_link,
        'thumbnail_url': asset_url(project.thumbnail_url),
        'created_at': project.created_at.timestamp(),
    }


class ProjectsListResource(Resource):
    @ns_projects.response(200, "Successfully Retrieved Projects")
    @ns_projects.response(400, "Unable to Retrieve Projects")
    def get(self):
        try:
            projects = Projects.query.order_by(Projects.created_at.desc()).all()
            return [serialize_project(p) for p in projects], 200
        except Exception as e:
            app.logger.error(f"Error retrieving projects: {e}")
            return error_response(400, "Unable to Retrieve Projects")

    @jwt_required()
    @ns_projects.expect(create_project_model, validate=True)
    @ns_projects.response(201, "Successfully Created Project")
    @ns_projects.response(400, "Unable to Create Project")
    def post(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            title = data.get('title')

            if not user_id or not title:
                return error_response(400, "user_id and title are required")

            user = Users.query.filter_by(id=user_id).first()
            if not user:
                return error_response(404, "User not found")

            new_project = Projects(
                user_id=user_id,
                title=title,
                description=data.get('description'),
                year=data.get('year'),
                contributions=data.get('contributions', []),
                tech_stack=data.get('tech_stack', []),
                github_link=data.get('github_link'),
                live_link=data.get('live_link'),
                thumbnail_url=data.get('thumbnail_url'),
            )
            db.session.add(new_project)
            db.session.commit()

            return serialize_project(new_project), 201

        except Exception as e:
            app.logger.error(f"Error creating project: {e}")
            return error_response(400, "Unable to Create Project")


class ProjectResource(Resource):
    @ns_projects.response(200, "Successfully Retrieved Project")
    @ns_projects.response(404, "Project not found")
    def get(self, project_id):
        try:
            project = Projects.query.filter_by(id=project_id).first()
            if not project:
                return error_response(404, "Project not found")
            return serialize_project(project), 200
        except Exception as e:
            app.logger.error(f"Error retrieving project {project_id}: {e}")
            return error_response(400, "Unable to Retrieve Project")

    @jwt_required()
    @ns_projects.expect(update_project_model, validate=True)
    @ns_projects.response(200, "Successfully Updated Project")
    @ns_projects.response(400, "Unable to Update Project")
    def put(self, project_id):
        try:
            data = request.get_json()
            project = Projects.query.filter_by(id=project_id).first()
            if not project:
                return error_response(404, "Project not found")

            project.title = data.get('title', project.title)
            project.description = data.get('description', project.description)
            project.year = data.get('year', project.year)
            project.contributions = data.get('contributions', project.contributions)
            project.tech_stack = data.get('tech_stack', project.tech_stack)
            project.github_link = data.get('github_link', project.github_link)
            project.live_link = data.get('live_link', project.live_link)
            project.thumbnail_url = data.get('thumbnail_url', project.thumbnail_url)
            db.session.commit()

            return serialize_project(project), 200

        except Exception as e:
            app.logger.error(f"Error updating project {project_id}: {e}")
            return error_response(400, "Unable to Update Project")

    @jwt_required()
    @ns_projects.response(200, "Successfully Deleted Project")
    @ns_projects.response(404, "Project not found")
    def delete(self, project_id):
        try:
            project = Projects.query.filter_by(id=project_id).first()
            if not project:
                return error_response(404, "Project not found")

            db.session.delete(project)
            db.session.commit()
            return {"message": "Successfully Deleted Project"}, 200

        except Exception as e:
            app.logger.error(f"Error deleting project {project_id}: {e}")
            return error_response(400, "Unable to Delete Project")


ns_projects.add_resource(ProjectsListResource, '/', endpoint='projects-list')
ns_projects.add_resource(ProjectResource, '/<string:project_id>', endpoint='project')
