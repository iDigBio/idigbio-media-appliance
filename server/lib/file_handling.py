import os
import sys
import hashlib
import datetime

from app import db

file_types = {
    "jpg": ("images", "image/jpeg"),
    "mp3": ("sounds", "audio/mp3"),
    "mp4": ("videos", "video/mp4"),
    "stl": ("models", "model/mesh")
}


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
        with open(f, "rb") as fd:
            md5, size = do_hash(fd)
    else:
        md5, size = do_hash(f)

    if return_size:
        return (md5.hexdigest(), size)
    else:
        return md5.hexdigest()


def process_media(m, update_db=True):
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