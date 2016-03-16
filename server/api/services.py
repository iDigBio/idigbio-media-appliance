import sys

import multiprocessing

import easygui

from models import Media, Batch

from flask import Blueprint, request, jsonify

from lib.workwork import do_run_db

service_api = Blueprint("service_api", __name__)

worker = None


@service_api.route("/process")
def process():
    from app import db

    global worker
    c = db.session.query(Media).filter(
        db.or_(Media.status == None, Media.status != "uploaded")).count()  # noqa
    if worker is not None and worker.is_alive():
        res = jsonify({"status": "OK", "count": c})
    else:
        worker = multiprocessing.Process(target=do_run_db)
        worker.start()
        res = jsonify({"status": "OK", "count": c})
        res.status_code = 201
    return res


@service_api.route("/dirprompt")
def dirprompt():
    return jsonify({
        "path": easygui.diropenbox()
    })


@service_api.route("/fileprompt")
def fileprompt():
    return jsonify({
        "path": easygui.filesavebox(default="media.csv")
    })
