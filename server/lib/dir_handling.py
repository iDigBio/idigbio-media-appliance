import os
import uuid
import re
import datetime

from functools import partial

from lib.file_handling import file_types, calcFileHash

from models import Media
from api.appuser import get_current_user

guid_mode = {
    "regex": lambda regex, tmpl, path: regex.match(path).expand(tmpl),
    "uuid": lambda path: str(uuid.uuid4()),
    "hash": lambda path: calcFileHash(path),
}


class NotAuthorizedException(Exception):
    pass


def scan_dir(directory, guid_type="uuid", guid_params=None):
    if guid_type == "regex":
        ref_func = partial(*guid_params)
    else:
        ref_func = guid_mode[guid_type]

    directory = os.path.abspath(directory)
    dir_objects = {m.path: m for m in Media.query.filter(
        Media.path.like(directory + "%")).all()}

    current_user = get_current_user()
    if current_user is None:
        raise NotAuthorizedException

    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.rsplit(".", 1)[-1] in file_types:
                    p = os.path.join(root, f)
                    m = None
                    if p in dir_objects:
                        m = dir_objects[p]
                        if m.status == "uploaded":
                            h = calcFileHash(p)
                            if m.image_hash == h:
                                continue
                            m.status = "file_changed"
                            m.status_date = datetime.datetime.now()
                            m.status_detail = m.image_hash
                            m.image_hash = h
                            m.appuser = current_user
                            if guid_type == "hash":
                                m.file_reference = h
                    else:
                        m = Media(path=p, file_reference=ref_func(p),
                                  appuser=current_user)

                    yield m
    else:
        raise FileNotFoundError("No Such Directory {}".format(directory))

if __name__ == '__main__':
    for m in scan_dir("/home/godfoder/Downloads"):
        print(m)
