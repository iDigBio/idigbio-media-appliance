import os
import logging

logging.root.setLevel(logging.DEBUG)
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

from gevent.pool import Pool
from functools import partial
from itertools import islice
from lib.file_handling import process_media
from lib.dir_handling import scan_dir
from models import Media
from app import db


def do_run_db():
    logging.info("DB Run Started")
    p = Pool(50)

    last_i = 0
    pm_no_update = partial(process_media,update_db=False)
    for i, m in enumerate(p.imap_unordered(pm_no_update, db.session.query(Media).filter(db.or_(Media.status == None, Media.status != "uploaded")))):
        last_i = i+1
        db.session.add(m)
        if i % 1000 == 0:
            logging.debug("upload group {}".format(i))
            db.session.commit()
    logging.info("DB Run Finished: {} records processed".format(last_i))
    db.session.commit()

def do_create_media(directory, guid_type="uuid", guid_params=None):
    last_i = 0
    for i, m in enumerate(scan_dir(directory, guid_type=guid_type, guid_params=guid_params)):
        last_i = i+1
        db.session.add(m)
        if i % 1000 == 0:
            logging.debug("scan group {}".format(i))
            db.session.commit()
    logging.info("Directory Scan Finished: {} new+updates".format(last_i))
    db.session.commit()

if __name__ == '__main__':
    do_create_media("/media/godfoder/BISH_2/raw_media_archive_jpg")
    # pid = os.getpid()
    # logging.info("Processing job {} started.".format(pid))
    # do_run_db()
    # logging.info("Processing job {} ended.".format(pid))