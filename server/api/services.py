import sys

from models import Media, Batch

from flask import Blueprint, request, jsonify

service_api = Blueprint("service_api", __name__)

from lib.workwork import do_run_db
import multiprocessing

import easygui

worker = None

@service_api.route("/process")
def process():
    from app import db

    global worker
    c = db.session.query(Media).filter(db.or_(Media.status == None, Media.status != "uploaded")).count()
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
        "path": easygui.fileopenbox()
    })