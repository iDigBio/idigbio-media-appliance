import os
import appdirs
basedir = os.path.abspath(os.path.dirname(__file__))

USER_DATA = appdirs.user_data_dir("media_appliance", "idigbio")

if not os.path.exists(USER_DATA):
    os.makedirs(USER_DATA)

DATABASE_FILE = os.path.join(USER_DATA, "local.db")

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(DATABASE_FILE)

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
