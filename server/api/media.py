from flask import Blueprint, request
from flask_restful import Api, Resource
from models import Media

media_api = Api(Blueprint("media_api", __name__))

@media_api.resource("/media")
class MediaAPI(Resource):

    @staticmethod
    def get():
        return {
            "count": Media.query.count(),
            "media": [
                {
                    "id": media.id,
                    "path": media.path,
                    "media_type": media.media_type,
                    "mime": media.mime,
                    "file_reference": media.file_reference,
                    "image_hash": media.image_hash,
                    "uploaded": media.uploaded,
                    "uploaded_date": media.uploaded_date.isoformat()
                } for media in Media.query
            ]
        }

    @staticmethod
    def post():
        from app import db

        print(request.headers)

        b = request.get_json()

        media = Media()
        media.path = b["path"]
        media.file_reference = b["file_reference"]

        if "media_type" in b:
            media.media_type = b["media_type"]

        if "mime" in b:
            media.mime = b["mime"]

        if "image_hash" in b:
            media.image_hash = b["image_hash"]

        db.session.add(media)
        db.session.commit()
 
        return {
            "id": media.id,
            "path": media.path,
            "media_type": media.media_type,
            "mime": media.mime,            
            "file_reference": media.file_reference,
            "image_hash": media.image_hash,
            "uploaded": media.uploaded,
            "uploaded_date": media.uploaded_date.isoformat()
        }

@media_api.resource("/media/<int:media_id>")
class MediaItemAPI(Resource):

    @staticmethod
    def get(media_id):
        from app import db

        media = Media.query.get_or_404(media_id)

        return {
            "id": media.id,
            "path": media.path,
            "media_type": media.media_type,
            "mime": media.mime,            
            "file_reference": media.file_reference,
            "image_hash": media.image_hash,
            "uploaded": media.uploaded,
            "uploaded_date": media.uploaded_date.isoformat()
        }