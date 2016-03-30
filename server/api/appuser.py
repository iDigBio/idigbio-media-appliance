from __future__ import absolute_import, print_function, division, unicode_literals

import json
import datetime

from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

from ..models import AppUser

appuser_api = Api(Blueprint("appuser_api", __name__))


def filter_config(b):
    for k in list(b.keys()):
        if k in ["user_uuid", "auth_key", "user_alias"]:
            del b[k]


def get_current_user():
    from ..app import db

    return db.session.query(AppUser).filter(AppUser.login_date != None).order_by(  # noqa
            AppUser.login_date.desc()).first()


@appuser_api.blueprint.before_app_request
def set_current_user():
    from ..app import db

    g.appuser = get_current_user()


@appuser_api.resource("/appuser")
class AppUserAPI(Resource):

    @staticmethod
    def get():
        u = g.appuser

        if u is not None:
            c = {}
            c.update(json.loads(u.config))
            c["id"] = u.id
            c["user_alias"] = u.user_alias
            c["user_uuid"] = u.user_uuid

            return jsonify(c)
        else:
            j = jsonify({"error": "Not Authorized"})
            j.status_code = 401
            return j

    @staticmethod
    def post():
        from ..app import db

        b = request.get_json()

        u = db.session.query(AppUser).filter(
            AppUser.user_uuid == b["user_uuid"]).first()

        if u is None:
            u = AppUser()
            u.user_uuid = b["user_uuid"]
            if "user_alias" in b:
                u.user_alias = b["user_alias"]

            if "auth_key" in b:
                u.auth_key = b["auth_key"]

            u.config = "{}"
            u.login_date = datetime.datetime.now()
        else:
            if "auth_key" in b:
                # Validate API Key against API?
                u.auth_key = b["auth_key"]

            if "user_alias" in b:
                u.user_alias = b["user_alias"]

            filter_config(b)
            d = json.loads(u.config)
            d.update(b)
            u.config = json.dumps(d)

            u.login_date = datetime.datetime.now()

        db.session.add(u)
        db.session.commit()

        c = {}
        c.update(json.loads(u.config))
        c["id"] = u.id
        c["user_uuid"] = u.user_uuid
        c["user_alias"] = u.user_alias

        return jsonify(c)

    @staticmethod
    def delete():
        from ..app import db

        u = db.session.query(AppUser).filter(AppUser.login_date != None).order_by(  # noqa
            AppUser.login_date.desc()).first()
        if u is not None:
            u.login_date = None

            db.session.add(u)
            db.session.commit()

        return jsonify({})

# @appuser_api.resource("/user/<int:user_id>")
# class AppUserConfig(Resource):

#     @staticmethod
#     def get():
#         u = AppUser.query.get_or_404(user_id)

#         c = {}
#         c.update(json.loads(u.config))
#         c["id"] = u.id
#         c["user_uuid"] = u.user_uuid

#         return jsonify(C)

#     @staticmethod
#     def post():
#         from app import db

#         u = AppUser.query.get_or_404(user_id)

#         b = request.get_json()

#         filter_config(b)

#         u.config = json.dumps(b)

#         db.session.add(u)
#         db.session.commit()

#         c = {}
#         c.update(json.loads(u.config))
#         c["id"] = u.id
#         c["user_uuid"] = u.user_uuid

#         return jsonify(c)
