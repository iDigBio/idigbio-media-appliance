import os
import logging
import csv
import uuid
import json

from pathlib import Path
from urllib.parse import urlparse, unquote
from config import basedir
from gevent.pool import Pool
from functools import partial
from itertools import islice
from collections import Counter
from lib.file_handling import process_media, check_update
from lib.dir_handling import scan_dir
from models import Media
from app import db, app
from api.appuser import get_current_user

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

    with open(in_file_path, "r") as in_f:
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


def do_run_db():
    logging.info("DB Run Started")
    p = Pool(50)

    last_i = 0
    pm_no_update = partial(process_media, update_db=False)
    media_query = db.session.query(Media).filter(
        db.or_(Media.status == None, Media.status != "uploaded"))  # noqa
    for i, m in enumerate(p.imap_unordered(pm_no_update, media_query)):
        last_i = i + 1
        db.session.add(m)
        if i % 1000 == 0:
            logging.debug("upload group {}".format(i))
            db.session.commit()
    logging.info("DB Run Finished: {} records processed".format(last_i))
    db.session.commit()


def do_create_media(directory, guid_type="uuid", guid_params=None,
                    add_to_db=True, out_file_name=None, recursive=True):

    out_file = None
    writer = None
    if not add_to_db:
        if out_file_name is None:
            out_file_name = str(uuid.uuid4()) + ".csv"

        out_file = open(
                        os.path.join(
                            app.config["USER_DATA"],
                            out_file_name
                        ),
                        "w",
                        encoding="utf-8"
                    )
        writer = csv.writer(out_file)
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
    do_create_media("/media/godfoder/BISH_2/raw_media_archive_jpg")
    # pid = os.getpid()
    # logging.info("Processing job {} started.".format(pid))
    # do_run_db()
    # logging.info("Processing job {} ended.".format(pid))
