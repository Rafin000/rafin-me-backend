from functools import wraps
from flask import abort, request, current_app as app

def check_apikey(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.headers.get('Authorization').split(" ")[-1] if request.headers.get('Authorization') else None
        api_key = request.headers.get('API-KEY')
        app.logger.info(f"auth_token: {auth_token}")
        app.logger.info(f"api key: {api_key}")
        if not auth_token and not api_key:
            abort(404, "No token or api key found!!!")
        # elif auth_token:
        #     payload = User.decode_auth_token(auth_token)
        #     if payload == 'Signature expired. Please log in again.':
        #         abort(401, "Expired Token")
        #     elif payload == 'Invalid token. Please log in again.':
        #         abort(401, "Invalid Token")
        #     return f(*args, **kwargs)
        # else:
        if api_key != app.config.get("API_KEY"):
            abort(401, "Invalid Key")
        return f(*args, **kwargs)
    return decorated