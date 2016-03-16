import os
import appdirs
basedir = os.path.abspath(os.path.dirname(__file__))

user_data = appdirs.user_data_dir("media_appliance", "idigbio")

if not os.path.exists(user_data):
    os.mkdirs(user_data)

DATABASE_FILE = os.path.join(user_data, "local.db")

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(DATABASE_FILE)

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
