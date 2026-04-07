from flask_restx import Api
from flask_jwt_extended.exceptions import (
    NoAuthorizationError,
    InvalidHeaderError,
    JWTDecodeError,
    WrongTokenError,
    RevokedTokenError,
    FreshTokenRequired,
    CSRFError,
    UserLookupError,
)
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from project.server.api.blog.views import ns_blog
from project.server.api.user.views import ns_user
from project.server.api.social.views import ns_social
from project.server.api.testimonial.views import ns_testimonial
from project.server.api.skill.views import ns_user_skill
from project.server.api.mail.views import ns_mail
from project.server.api.BlogTag.views import ns_blog_tags
from project.server.api.Education.views import ns_education
from project.server.api.Experience.views import ns_experience
from project.server.api.auth.views import ns_auth
from project.server.api.uploads.views import ns_uploads

api_blog = Api(version='1.0', title='Blog Service API', prefix='/api/v1', doc='/docs')
api_blog.add_namespace(ns_blog, path='/blogs')
api_blog.add_namespace(ns_user, path='/users')
api_blog.add_namespace(ns_social, path='/socials')
api_blog.add_namespace(ns_testimonial, path='/testimonials')
api_blog.add_namespace(ns_user_skill, path='/skills')
api_blog.add_namespace(ns_mail, path='/mails')
api_blog.add_namespace(ns_blog_tags, path='/blogs-tag')
api_blog.add_namespace(ns_education, path='/education')
api_blog.add_namespace(ns_experience, path='/experience')
api_blog.add_namespace(ns_auth, path='/auth')
api_blog.add_namespace(ns_uploads, path='/uploads')


# Translate flask-jwt-extended exceptions into proper HTTP responses
# (otherwise flask-restx swallows them and returns 500).
@api_blog.errorhandler(NoAuthorizationError)
def _handle_no_auth(error):
    return {"message": "Missing Authorization header"}, 401


@api_blog.errorhandler(InvalidHeaderError)
def _handle_invalid_header(error):
    return {"message": "Invalid Authorization header"}, 401


@api_blog.errorhandler(JWTDecodeError)
def _handle_jwt_decode(error):
    return {"message": "Invalid token"}, 401


@api_blog.errorhandler(WrongTokenError)
def _handle_wrong_token(error):
    return {"message": "Wrong token type"}, 401


@api_blog.errorhandler(RevokedTokenError)
def _handle_revoked_token(error):
    return {"message": "Token has been revoked"}, 401


@api_blog.errorhandler(FreshTokenRequired)
def _handle_fresh_required(error):
    return {"message": "Fresh token required"}, 401


@api_blog.errorhandler(CSRFError)
def _handle_csrf(error):
    return {"message": "CSRF check failed"}, 401


@api_blog.errorhandler(UserLookupError)
def _handle_user_lookup(error):
    return {"message": "User not found"}, 401


@api_blog.errorhandler(ExpiredSignatureError)
def _handle_expired(error):
    return {"message": "Token has expired"}, 401


@api_blog.errorhandler(InvalidTokenError)
def _handle_invalid_token(error):
    return {"message": "Invalid token"}, 401
