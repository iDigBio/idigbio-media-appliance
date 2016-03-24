import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import logging

# from gevent import monkey
# monkey.patch_all()

logging.root.setLevel(logging.DEBUG)
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import *  # noqa
from create_db import create_or_update_db  # noqa


def init_routes():
    from api.batch import batch_api
    from api.media import media_api
    from api.appuser import appuser_api
    from api.services import service_api
    from views.index import index_view

    app.register_blueprint(media_api.blueprint, url_prefix='/api')
    app.register_blueprint(batch_api.blueprint, url_prefix='/api')
    app.register_blueprint(appuser_api.blueprint, url_prefix='/api')
    app.register_blueprint(service_api, url_prefix='/api')
    app.register_blueprint(index_view)

if __name__ == '__main__':
    dbg = "True" == os.getenv("DEBUG", "False")
    init_routes()
    create_or_update_db()
    if dbg:
        # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        app.run(debug=True)
    else:
        app.run()
