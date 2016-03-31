from __future__ import absolute_import, print_function, division, unicode_literals

import os
import json
import datetime

from flask import Blueprint, request, g, jsonify
from flask_restful import Api, Resource
from ..models import Media

from .appuser import get_current_user

media_api = Api(Blueprint("media_api", __name__))


def format_status_date(media):
    status_date = None
    if media.status_date is not None:
        status_date = media.status_date.isoformat()

    return status_date


@media_api.resource("/media")
class MediaAPI(Resource):

    @staticmethod
    def get():
        from ..app import db

        current_user = get_current_user()

        try:
            o = int(request.args.get('offset', 0))
            l = int(request.args.get('limit', 100))
        except:
            res = jsonify({"error": "Limit and offset must be integers"})
            res.status_code = 400
            return res

        period = request.args.get('time_period', 'all')
        query = db.session.query(Media).filter(Media.appuser == current_user)

        last_date = None
        if period == "day":
            last_date = datetime.datetime.now() - datetime.timedelta(days=1)
        elif period == "week":
            last_date = datetime.datetime.now() - datetime.timedelta(days=7)
        elif period == "month":
            last_date = datetime.datetime.now() - datetime.timedelta(days=30)

        if last_date is not None:
            query = query.filter(Media.status_date > (last_date))

        return {
            "count": db.session.query(Media).filter(Media.appuser == current_user).count(),
            "media": [
                {
                    "id": media.id,
                    "path": media.path,
                    "media_type": media.media_type,
                    "mime": media.mime,
                    "file_reference": media.file_reference,
                    "props": json.loads(media.props),
                    "image_hash": media.image_hash,
                    "status": media.status,
                    "status_date": format_status_date(media),
                    "status_detail": media.status_detail
                } for media in query[o:o+l]
            ]
        }

    @staticmethod
    def post():
        from ..app import db

        if g.appuser is None:
            j = jsonify({"error": "Not Authorized"})
            j.status_code = 401
            return j

        b = request.get_json()

        media = Media()
        media.path = os.path.abspath(b["path"])
        media.file_reference = b["file_reference"]
        media.appuser = g.appuser

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
            "props": json.loads(media.props),
            "image_hash": media.image_hash,
            "status": media.status,
            "status_date": format_status_date(media),
            "status_detail": media.status_detail
        }


@media_api.resource("/media/<int:media_id>")
class MediaItemAPI(Resource):

    @staticmethod
    def get(media_id):
        from ..app import db

        media = Media.query.get_or_404(media_id)

        return {
            "id": media.id,
            "path": media.path,
            "media_type": media.media_type,
            "mime": media.mime,
            "file_reference": media.file_reference,
            "props": json.loads(media.props),
            "image_hash": media.image_hash,
            "status": media.status,
            "status_date": format_status_date(media),
            "status_detail": media.status_detail
        }


@media_api.resource("/media/status")
class MediaStatusAPI(Resource):

    @staticmethod
    def get():
        from ..app import db

        current_user = get_current_user()

        statuses = db.session.query(db.func.count('*').label(
            "c"), Media.status).filter(Media.appuser == current_user).group_by(Media.status).all()

        resp_d = {
            "count": db.session.query(Media).filter(Media.appuser == current_user).count()
        }

        for m in statuses:
            if m.status is None:
                resp_d["pending"] = m.c
            else:
                resp_d[m.status] = m.c

        return resp_d
