
from logging import getLogger, INFO, DEBUG

logger = getLogger()
logger.setLevel(DEBUG)

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
    from views.index import index_view

    app.register_blueprint(media_api.blueprint, url_prefix='/api')
    app.register_blueprint(batch_api.blueprint, url_prefix='/api')
    app.register_blueprint(index_view)

if __name__ == '__main__':
    dbg = "True" == os.getenv("DEBUG","False")
    init_routes()
    if dbg:
        logger.setLevel(DEBUG)
        app.run(debug=True)
    else:
        app.run()
