import os
import appdirs
import json

basedir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(basedir, "../package.json"), "r") as jf:
	package_config = json.load(jf)

USER_DATA = appdirs.user_data_dir("media_appliance", "idigbio")

if not os.path.exists(USER_DATA):
    os.makedirs(USER_DATA)

DATABASE_FILE = os.path.join(USER_DATA, "local.db")

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(DATABASE_FILE)

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')



APP_VERSION = package_config["version"]