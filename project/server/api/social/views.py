from flask import request, current_app as app
from flask_restx import Resource
from project.server.docorators import check_apikey
from project.server.models.models import SocialMediaLinks
from project.server.api.social.schema import *
from project.server.api.social import ns_social
from project.server import db
from project.server.utils import error_response


class SocialMediaLinksList(Resource):
    @check_apikey
    @ns_social.expect(create_social_media_links_model, validate=True)
    @ns_social.response(201, "Successfully Created Social Media Link")
    @ns_social.response(400, "Unable to Create Social Media Link")
    def post(self):
        try:
            data = request.get_json()
            social_media_link = SocialMediaLinks(
                user_id=data['user_id'],
                facebook=data.get('facebook'),
                linkedin=data.get('linkedin'),
                instagram=data.get('instagram'),
                github=data.get('github')
            )
            db.session.add(social_media_link)
            db.session.commit()
            return {"message": "Successfully Created Social Media Link"}, 201
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Create Social Media Link")

    # @check_apikey
    @ns_social.response(200, "Successfully Retrieved Social Media Links")
    @ns_social.response(400, "Unable to Retrieve Social Media Links")
    def get(self):
        try:
            links = SocialMediaLinks.query.all()
            serialized_links = [
                {
                    'id': str(link.id),
                    'user_id': str(link.user_id),
                    'facebook': link.facebook,
                    'linkedin': link.linkedin,
                    'instagram': link.instagram,
                    'github': link.github
                } for link in links
            ]
            return {"message": "Successfully Retrieved Social Media Links", "data": serialized_links}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Social Media Links")

class SocialMediaLink(Resource):
    # @check_apikey
    @ns_social.response(200, "Successfully Retrieved Social Media Link")
    @ns_social.response(400, "Unable to Retrieve Social Media Link")
    def get(self, link_id):
        try:
            link = SocialMediaLinks.query.filter_by(id=link_id).first()
            if not link:
                return error_response(400, "Social Media Link not found")

            serialized_link = {
                'id': str(link.id),
                'user_id': str(link.user_id),
                'facebook': link.facebook,
                'linkedin': link.linkedin,
                'instagram': link.instagram,
                'github': link.github
            }
            return {"message": "Successfully Retrieved Social Media Link", "data": serialized_link}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Retrieve Social Media Link")

    @check_apikey
    @ns_social.expect(update_social_media_links_model, validate=True)
    @ns_social.response(200, "Successfully Updated Social Media Link")
    @ns_social.response(400, "Unable to Update Social Media Link")
    def put(self, link_id):
        try:
            data = request.get_json()
            link = SocialMediaLinks.query.filter_by(id=link_id).first()

            if not link:
                return error_response(400, "Social Media Link not found")

            link.facebook = data.get('facebook', link.facebook)
            link.linkedin = data.get('linkedin', link.linkedin)
            link.instagram = data.get('instagram', link.instagram)
            link.github = data.get('github', link.github)
            
            db.session.commit()
            return {"message": "Successfully Updated Social Media Link"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Update Social Media Link")

    @check_apikey
    @ns_social.response(200, "Successfully Deleted Social Media Link")
    @ns_social.response(400, "Unable to Delete Social Media Link")
    def delete(self, link_id):
        try:
            link = SocialMediaLinks.query.filter_by(id=link_id).first()
            if not link:
                return error_response(400, "Social Media Link not found")

            db.session.delete(link)
            db.session.commit()
            return {"message": "Successfully Deleted Social Media Link"}, 200
        except Exception as e:
            app.logger.error(e)
            return error_response(400, "Unable to Delete Social Media Link")

ns_social.add_resource(SocialMediaLinksList, '/')
ns_social.add_resource(SocialMediaLink, '/<string:link_id>')
