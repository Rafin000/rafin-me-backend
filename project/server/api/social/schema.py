from flask_restx import fields, Model
from project.server.api.social import ns_social

create_social_media_links_type = Model('CreateSocialMediaLinks', {
    'user_id': fields.String(required=True, description='The ID of the user associated with these links'),
    'facebook': fields.String(description='Facebook profile URL'),
    'linkedin': fields.String(description='LinkedIn profile URL'),
    'instagram': fields.String(description='Instagram profile URL'),
    'github': fields.String(description='GitHub profile URL')
})


update_social_media_links_type = Model('UpdateSocialMediaLinks', {
    'facebook': fields.String(description='Facebook profile URL'),
    'linkedin': fields.String(description='LinkedIn profile URL'),
    'instagram': fields.String(description='Instagram profile URL'),
    'github': fields.String(description='GitHub profile URL')
})


create_social_media_links_model = ns_social.add_model('CreateSocialMediaLinks', create_social_media_links_type)
update_social_media_links_model = ns_social.add_model('UpdateSocialMediaLinks', update_social_media_links_type)