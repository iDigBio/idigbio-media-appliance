from __future__ import absolute_import, print_function, division, unicode_literals

import os
import logging

import io
import unicodecsv as csv
import uuid
import json
import idigbio

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path
try:
    from urllib.parse import urlparse, unquote
except ImportError:
    from urllib import unquote
    from urlparse import urlparse

from gevent.pool import Pool
from functools import partial
from itertools import islice
from collections import Counter

from . import get_uuid_unicode
from ..config import basedir
from .file_handling import process_media, check_update, type_dc_type
from .dir_handling import scan_dir
from ..models import Media
from ..app import db, app
from ..api.appuser import get_current_user

from gevent import monkey

logging.root.setLevel(logging.DEBUG)
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)


def combined(*args, **kwargs):
    kwargs["add_to_db"] = True
    do_create_media(*args, **kwargs)
    do_run_db()


def combined_load(*args, **kwargs):
    rv = load_csv(*args)
    do_run_db()
    return rv


def load_csv(in_file_path, metadata=None):
    logging.info("CSV Load of %s Started", in_file_path)
    d = {}
    if metadata is not None:
        d.update(metadata)
    stats = Counter()

    current_user = get_current_user()
    if current_user is None:
        raise NotAuthorizedException

    media_objects = {m.path: m for m in Media.query.all()}

    with io.open(in_file_path, "r") as in_f:
        reader = csv.DictReader(in_f)
        last_i = 0
        for i, l in enumerate(reader):
            last_i = i
            try:
                a_uri = l.get("ac:accessURI", "")
                if a_uri.startswith("file:///"):
                    path = os.path.abspath(unquote(urlparse(a_uri).path))
                else:
                    path = l["idigbio:OriginalFileName"]
                # Try recordID, get MediaGUID or raise key error as default

                guid = l.get("idigbio:recordID")
                if guid is None:
                    guid = l["idigbio:MediaGUID"]

                d.update(l)

                for k in [
                    "idigbio:MediaGUID",
                    "idigbio:recordID",
                    "idigbio:OriginalFileName",
                ]:
                    if k in d:
                        del d[k]

                if path in media_objects:
                    m = check_update(media_objects[path], path, current_user)
                else:
                    m = Media(
                        path=path,
                        file_reference=guid,
                        props=json.dumps(d),
                        appuser=current_user
                    )

                db.session.add(m)

                if i % 1000 == 0:
                    logging.debug("CSV Load Group {}".format(i))
                    db.session.commit()
            except KeyError:
                logging.exception("Key Error in record")
                stats["invalid"] += 1
            except:
                logging.exception("Exception in record")
                stats["error"] += 1
    db.session.commit()
    logging.info("CSV Load Finished: {} records processed".format(last_i + 1))
    return stats.most_common()


def get_api_client(current_user=None):
    if current_user is None:
        current_user = get_current_user()

    return idigbio.json(
        env="prod",
        user=current_user.user_uuid,
        password=current_user.auth_key
    )


def do_run_db():
    monkey.patch_all()
    logging.info("DB Run Started")
    p = Pool(20)

    current_user = get_current_user()
    if current_user is None:
        raise NotAuthorizedException()

    api = get_api_client(current_user=current_user)

    last_i = 0
    pm_no_update = partial(process_media, update_db=False, api=api)
    media_query = db.session.query(Media).filter(
        db.or_(Media.status == None, Media.status != "uploaded")).filter(
        Media.appuser == current_user)  # noqa
    for i, m in enumerate(p.imap_unordered(pm_no_update, media_query)):
        last_i = i + 1
        db.session.add(m)
        if i % 100 == 0:
            logging.debug("upload group {}".format(i))
            db.session.commit()
    logging.info("DB Run Finished: {} records processed".format(last_i))
    db.session.commit()

    out_file_name = media_csv()
    out_file = os.path.join(
        app.config["USER_DATA"],
        out_file_name
    )
    api.upload(
        "http://api.idigbio.org/v1/recordsets/{}".format(
            current_user.user_uuid
        ),
        out_file,
        media_type="datasets"
    )


def media_csv(period=None, out_file_name=None):
    query = db.session.query(Media)

    last_date = None
    if period == "day":
        last_date = datetime.datetime.now() - datetime.timedelta(days=1)
    elif period == "week":
        last_date = datetime.datetime.now() - datetime.timedelta(days=7)
    elif period == "month":
        last_date = datetime.datetime.now() - datetime.timedelta(days=30)

    if last_date is not None:
        query = query.filter(Media.status_date > (last_date))

    if out_file_name is None:
        out_file_name = get_uuid_unicode() + ".csv"

    with io.open(
        os.path.join(
            app.config["USER_DATA"],
            out_file_name
        ),
        "wb"
    ) as out_file:
        writer = csv.writer(out_file, encoding="utf-8")
        writer.writerow([
            "idigbio:recordID",
            "ac:accessURI",
            "dc:type",
            "dc:format",
            "idigbio:OriginalFileName",
            "ac:hashFunction",
            "ac:hashValue",
            "idigbio:jsonProperties",
            "idigbio:mediaStatus",
            "idigbio:mediaStatusDate",
            "idigbio:mediaStatusDetail"
        ])

        for m in query.all():
            if m.media_type in type_dc_type:
                dc_type = type_dc_type[m.media_type]
            else:
                dc_type = ""

            if m.status == "uploaded":
                writer.writerow([
                    m.file_reference,
                    "http://media.idigbio.org/" + m.image_hash,
                    dc_type,
                    m.mime,
                    m.path,
                    "md5",
                    m.image_hash,
                    m.props,
                    m.status,
                    m.status_date,
                    m.status_detail
                ])
            else:
                writer.writerow([
                    m.file_reference,
                    "",
                    dc_type,
                    m.mime,
                    m.path,
                    "md5",
                    m.image_hash,
                    m.props,
                    m.status,
                    m.status_date,
                    m.status_detail
                ])

    return out_file_name


def do_create_media(directory, guid_type="uuid", guid_params=None,
                    add_to_db=True, out_file_name=None, recursive=True):

    out_file = None
    writer = None
    if not add_to_db:
        if out_file_name is None:
            out_file_name = get_uuid_unicode() + ".csv"

        out_file = io.open(
                        os.path.join(
                            app.config["USER_DATA"],
                            out_file_name
                        ),
                        "wb"
                    )
        writer = csv.writer(out_file, encoding="utf-8")
        writer.writerow(["idigbio:recordID", "ac:accessURI"])

    last_i = 0
    for i, m in enumerate(scan_dir(directory, guid_type=guid_type, guid_params=guid_params, recursive=recursive)):  # noqa
        last_i = i + 1
        if add_to_db:
            db.session.add(m)
        else:
            writer.writerow([m.file_reference, Path(m.path).as_uri()])

        if i % 1000 == 0:
            logging.debug("scan group {}".format(i))
            if add_to_db:
                db.session.commit()
    logging.info("Directory Scan Finished: {} new+updates".format(last_i))

    if add_to_db:
        db.session.commit()
    else:
        out_file.close()

    return out_file_name


if __name__ == '__main__':
    print(media_csv())
