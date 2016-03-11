
import logging

from gevent import monkey
monkey.patch_all()

logging.root.setLevel(logging.DEBUG)
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import models

def init_routes():
    from api.batch import batch_api
    from api.media import media_api
    from api.services import service_api
    from views.index import index_view

    app.register_blueprint(media_api.blueprint, url_prefix='/api')
    app.register_blueprint(batch_api.blueprint, url_prefix='/api')
    app.register_blueprint(service_api, url_prefix='/api')
    app.register_blueprint(index_view)

if __name__ == '__main__':
    dbg = "True" == os.getenv("DEBUG","False")
    init_routes()
    if dbg:
        app.run(debug=True)
    else:
        app.run()
