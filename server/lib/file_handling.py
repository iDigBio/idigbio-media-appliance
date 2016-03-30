from __future__ import absolute_import, print_function, division, unicode_literals

import os
import io
import sys
import hashlib
import datetime

from ..app import db

file_types = {
    "jpg": ("images", "image/jpeg"),
    "mp3": ("sounds", "audio/mp3"),
    "mp4": ("videos", "video/mp4"),
    "stl": ("models", "model/mesh")
}

type_dc_type = {
    "images": "StillImage",
    "sounds": "Sound",
    "videos": "MovingImage",
    "models": "InteractiveResource"
}


def check_update(m, p, current_user, guid_type=None):
    h = calcFileHash(p)
    if m.image_hash == h:
        return m
    m.status = "file_changed"
    m.status_date = datetime.datetime.now()
    m.status_detail = m.image_hash
    m.image_hash = h
    m.appuser = current_user
    if guid_type == "hash":
        m.file_reference = h
    return m


def calcFileHash(f, op=True, return_size=False, read_size=2048):
    def do_hash(fd):
        md5 = hashlib.md5()
        size = 0

        buf = fd.read(read_size)
        while len(buf) > 0:
            size += len(buf)
            md5.update(buf)
            buf = fd.read(read_size)

        return md5, size

    if op:
        with io.open(f, "rb") as fd:
            md5, size = do_hash(fd)
    else:
        md5, size = do_hash(f)

    if return_size:
        return (md5.hexdigest(), size)
    else:
        return md5.hexdigest()


def process_media(m, update_db=True, api=None):
    try:
        if os.path.exists(m.path):
            h, size = calcFileHash(m.path, return_size=True)
            m.image_hash = h

            for k in file_types:
                if m.path.endswith(k):
                    m.media_type, m.mime = file_types[k]
                    break
            else:
                raise TypeError("Invalid File Type {}".format())

        else:
            raise FileNotFoundError

        # Upload Media File
        if api is None:
            m.status = "uploaded"
            m.status_date = datetime.datetime.now()
            m.status_detail = ""
        else:
            res = api.upload(m.file_reference, m.path)
            if res is None:
                m.status = "failed"
                m.status_date = datetime.datetime.now()
                m.status_detail = ""
            else:
                m.status = "uploaded"
                m.status_date = datetime.datetime.now()
                m.status_detail = ""

        if update_db:
            db.session.add(m)
            db.session.commit()

    except FileNotFoundError:
        e = sys.exc_info()[1]
        m.status = "missing"
        m.status_date = datetime.datetime.now()
        m.status_detail = repr(e)

    return m
