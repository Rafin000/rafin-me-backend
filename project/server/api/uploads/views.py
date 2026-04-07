import os
import uuid
from flask import current_app as app
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required
from werkzeug.datastructures import FileStorage

from project.server.api.uploads import ns_uploads
from project.server.utils import error_response, asset_url


ALLOWED_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg',
}

upload_parser = ns_uploads.parser()
upload_parser.add_argument(
    'file',
    location='files',
    type=FileStorage,
    required=True,
    help='Image file to upload',
)


def _get_s3_client():
    """Lazy-import boto3 and build a client from app config."""
    import boto3

    access_key = app.config.get('AWS_ACCESS_KEY_ID')
    secret_key = app.config.get('AWS_SECRET_ACCESS_KEY')
    region = app.config.get('AWS_REGION', 'us-east-1')
    bucket = app.config.get('S3_BUCKET')

    if not (access_key and secret_key and bucket):
        return None, None

    client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )
    return client, bucket


class UploadResource(Resource):
    @jwt_required()
    @ns_uploads.expect(upload_parser)
    @ns_uploads.response(201, 'Upload successful')
    @ns_uploads.response(400, 'Bad request')
    @ns_uploads.response(503, 'Upload service not configured')
    def post(self):
        s3, bucket = _get_s3_client()
        if s3 is None:
            return error_response(
                503,
                'Upload service not configured. Set AWS_ACCESS_KEY_ID, '
                'AWS_SECRET_ACCESS_KEY, and S3_BUCKET in the environment.',
            )

        args = upload_parser.parse_args()
        file = args.get('file')
        if not file or not file.filename:
            return error_response(400, 'No file provided')

        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return error_response(
                400,
                f'Unsupported file type: {ext}. Allowed: {sorted(ALLOWED_EXTENSIONS)}',
            )

        # Generate a UUID-based key so we never collide
        key_filename = f'{uuid.uuid4().hex}{ext}'
        prefix = (app.config.get('S3_UPLOAD_PREFIX') or '').strip('/')
        full_key = f'{prefix}/{key_filename}' if prefix else key_filename

        content_type = file.content_type or 'application/octet-stream'

        try:
            s3.upload_fileobj(
                file.stream,
                bucket,
                full_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': 'public, max-age=31536000, immutable',
                },
            )
        except Exception as e:
            app.logger.error(f'S3 upload failed: {e}')
            return error_response(500, 'Upload failed')

        return {
            'key': full_key,
            'url': asset_url(full_key),
        }, 201


ns_uploads.add_resource(UploadResource, '/')
