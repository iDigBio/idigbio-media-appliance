import sys

import multiprocessing

import easygui
import traceback
import uuid

from models import Media, Batch

from flask import Blueprint, request, current_app, jsonify, send_from_directory

from lib.workwork import do_run_db, do_create_media, combined


service_api = Blueprint("service_api", __name__)


tasks = {}

p = None


@service_api.route("/readdir", methods=["POST"])
def readdir():
    from app import db

    global p
    if p is None:
        p = multiprocessing.Pool(5)

    b = request.get_json()

    print(b)

    if b is None:
        j = jsonify({"error": "Missing JSON Request Body"})
        j.status_code = 400
        return j

    upload_path = None
    if "upload_path" in b:
        upload_path = b["upload_path"]
    else:
        j = jsonify({"error": "Missing upload_path"})
        j.status_code = 400
        return j

    upload = False
    if "upload" in b:
        upload = b["upload"] is True

    task_id = str(uuid.uuid4())

    current_app.logger.debug("Starting Worker %s", upload_path)
    if upload:
        tasks[task_id] = p.apply_async(
            combined,
            (upload_path,),
            {
                "out_file_name": task_id + ".csv"
            }
        )
        tasks["db_upload"] = tasks[task_id]
    else:
        tasks[task_id] = p.apply_async(
            do_create_media,
            (upload_path,),
            {
                "add_to_db": False,
                "out_file_name": task_id + ".csv"
            }
        )
    res = jsonify({"status": "STARTED", "task_id": task_id})
    res.status_code = 201

    return res


@service_api.route("/getfile/<string:filename>", methods=["GET"])
def return_readdir_file(filename):
    return send_from_directory(
        current_app.config["USER_DATA"],
        filename,
        as_attachment=True
    )


@service_api.route("/readdir/<string:task_id>", methods=["GET"])
def check_readdir_task(task_id):
    from app import db

    read_worker = None
    if task_id in tasks:
        read_worker = tasks[task_id]

    if read_worker is None:
        res = jsonify({"status": "ERROR", "error": "Task Not Found"})
        res.status_code = 404
    elif read_worker.ready():
        try:
            csv_file_name = read_worker.get()

            res = jsonify({
                "status": "DONE",
                "filename": csv_file_name,
                "task_id": task_id
            })
        except Exception as e:
            current_app.logger.exception("Error in readdir")
            del tasks[task_id]
            res = jsonify({"status": "ERROR", "error": str(e),
                           "task_id": task_id})
            res.status_code = 500
    else:
        res = jsonify({"status": "RUNNING", "task_id": task_id})

    return res


@service_api.route("/process")
def process():
    from app import db

    start = True
    try:
        start = request.args.get("start", "true") == "true"
    except:
        pass

    global p
    if p is None:
        p = multiprocessing.Pool(5)

    db_worker = None
    if "db_worker" in tasks:
        db_worker = tasks["db_worker"]

    c = db.session.query(Media).filter(
        db.or_(Media.status == None, Media.status != "uploaded")).count()  # noqa
    if db_worker is None:
        if start:
            current_app.logger.debug("Starting DB Worker")
            tasks["db_worker"] = p.apply_async(do_run_db)
            res = jsonify({
                "status": "STARTED",
                "count": c
            })
            res.status_code = 201
        else:
            res = jsonify({
                "status": "ENDED"
            })
            res.status_code = 200
    elif db_worker.ready():
        try:
            db_worker.get()
            del tasks["db_worker"]
            current_app.logger.debug("DB Upload Done")
            res = jsonify({"status": "ENDED"})
        except Exception as e:
            current_app.loggger.exception("Error in process")
            del tasks["db_worker"]
            res = jsonify({"status": "ERROR", "error": str(e)})
            res.status_code = 500
    else:
        res = jsonify({
            "status": "RUNNING",
            "count": c
        })

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
