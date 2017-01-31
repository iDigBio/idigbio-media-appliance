import os
import appdirs
import json
from .version import VERSION

basedir = os.path.abspath(os.path.dirname(__file__))

USER_DATA = appdirs.user_data_dir("media_appliance", "idigbio")

if not os.path.exists(USER_DATA):
    os.makedirs(USER_DATA)

# On Windows 7, the db will typically end up in C:\Users\<user>\AppData\Local\idigbio\media_appliance
# The "AppData" folder is not visible by default, use "Folder Options" to "Show all folders" in Navigation Pane
DATABASE_FILE = os.path.join(USER_DATA, "local.db")

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(DATABASE_FILE)

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')



APP_VERSION = VERSION
