from __future__ import absolute_import, print_function, division, unicode_literals

import sys
import os

import multiprocessing

import easygui
import traceback
import uuid
import re

from flask import Blueprint, request, current_app, jsonify, send_from_directory, redirect  # noqa

from ..models import Media

from ..lib import get_uuid_unicode
from ..lib.workwork import do_run_db, do_create_media, combined, combined_load, media_csv
from ..lib.dir_handling import guid_mode


service_api = Blueprint("service_api", __name__)


tasks = {}

p = None


@service_api.route("/shutdown")
def shutdown():
    if p is not None:
        p.terminate()
        p.join()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return jsonify({"shutdown": True})


@service_api.route("/mediacsv", methods=["POST"])
def genmediacsv():
    global p
    if p is None:
        p = multiprocessing.Pool(5)

    task_id = get_uuid_unicode()

    tasks[task_id] = p.apply_async(
        media_csv,
        [],
        {
            "period": request.args.get("period"),
            "out_file_name": task_id + ".csv"
        }
    )

    res = jsonify({"status": "STARTED", "task_id": task_id})
    res.status_code = 201

    return res


@service_api.route("/loadcsv", methods=["POST"])
def loadcsv():
    global p
    if p is None:
        p = multiprocessing.Pool(5)

    if "csv_path" not in request.files:
        res = jsonify({"error": "File Not Sent"})
        res.status_code = 400
        return res

    task_id = get_uuid_unicode()

    fname = os.path.join(
        current_app.config["USER_DATA"],
        task_id + ".csv"
    )

    request.files["csv_path"].save(fname)

    tasks[task_id] = p.apply_async(
        combined_load,
        (fname,),
        {
            "metadata": {
                "license": request.form["license"]
            }
        }
    )
    tasks["db_upload"] = tasks[task_id]

    return redirect("/#history-tab")


@service_api.route("/readdir", methods=["POST"])
def readdir():
    global p
    if p is None:
        p = multiprocessing.Pool(5)

    b = request.get_json()

    print(b)

    if b is None:
        j = jsonify({"error": "Missing JSON Request Body"})
        j.status_code = 400
        return j

    upload_path = b.get("upload_path")
    if upload_path is None:
        j = jsonify({"error": "Missing upload_path"})
        j.status_code = 400
        return j

    upload = b.get("upload", False)
    recursive = b.get("recursive", True)
    guid_syntax = b.get("guid_syntax", "uuid")

    if guid_syntax not in guid_mode:
        j = jsonify({"error": "Invalid GUID Syntax"})
        j.status_code = 400
        return j

    guid_prefix = b.get("guid_prefix")
    guid_params = None
    if guid_prefix is not None:
        guid_params = (guid_prefix + "\\1", )

    task_id = get_uuid_unicode()

    current_app.logger.debug("Starting Worker %s", upload_path)
    if upload:
        tasks[task_id] = p.apply_async(
            combined,
            (upload_path,),
            {
                "out_file_name": task_id + ".csv",
                "recursive": recursive,
                "guid_type": guid_syntax,
                "guid_params": guid_params,
            }
        )
        tasks["db_upload"] = tasks[task_id]
    else:
        tasks[task_id] = p.apply_async(
            do_create_media,
            (upload_path,),
            {
                "add_to_db": False,
                "out_file_name": task_id + ".csv",
                "recursive": recursive,
                "guid_type": guid_syntax,
                "guid_params": guid_params,
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
@service_api.route("/status/<string:task_id>", methods=["GET"])
def check_readdir_task(task_id):
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
    from ..app import db

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
            current_app.logger.exception("Error in process")
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
    dirname = request.args.get("dirname")
    return jsonify({
        "path": easygui.diropenbox(default=dirname)
    })


@service_api.route("/fileprompt")
def fileprompt():
    return jsonify({
        "path": easygui.filesavebox(default="media.csv")
    })
