import json
import datetime

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from models import User

user_api = Api(Blueprint("user_api", __name__))

def filter_config(b):
    for k in list(b.keys()):
        if k in ["user_uuid", "auth_key"]:
            del b[k]

@user_api.resource("/user")
class MediaAPI(Resource):

    @staticmethod
    def get():
        from app import db

        u = db.session.query(User).filter(User.login_date != None).order_by(User.login_date.desc()).first()

        if u is not None:
            c = {}
            c.update(json.loads(u.config))
            c["user_uuid"] = u.user_uuid

            return jsonify(c)
        else:
            j = jsonify({})
            #j.status_code = 401
            return j

    @staticmethod
    def post():
        from app import db

        b = request.get_json()

        u = db.session.query(User).filter(User.login_date != None).filter(User.user_uuid == b["user_uuid"]).first()

        print(b,u)

        if u is None:
            u = User()
            u.user_uuid = b["user_uuid"]
            u.auth_key = b["auth_key"]
            u.config = "{}"
            u.login_date = datetime.datetime.now()
        else:
            # Validate API Key against API?
            u.auth_key = b["auth_key"]

            u.login_date = datetime.datetime.now()

        db.session.add(u)
        db.session.commit()

    @staticmethod
    def delete():
        from app import db

        u = db.session.query(User).filter(User.login_date != None).order_by(User.login_date.desc()).first()
        if u is not None:
            u.login_date = None

            db.session.add(u)
            db.session.commit()

        return jsonify({})

@user_api.resource("/user/<int:user_id>")
class UserConfig(Resource):

    @staticmethod
    def get():
        u = User.query.get_or_404(user_id)

        c = {}
        c.update(json.loads(u.config))
        c["user_uuid"] = u.user_uuid

        return jsonify(C)

    @staticmethod
    def post():
        from app import db
 
        u = User.query.get_or_404(user_id)

        b = request.get_json()

        filter_config(b)

        u.config = json.dumps(b)

        db.session.add(u)
        db.session.commit()

        c = {}
        c.update(json.loads(u.config))
        c["user_uuid"] = u.user_uuid

        return jsonify(c)