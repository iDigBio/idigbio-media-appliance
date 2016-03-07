
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def create_app():
    from api.batch import batch_api
    from views.index import index_view

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL","sqlite://")

    app.register_blueprint(batch_api.blueprint, url_prefix='/api')
    app.register_blueprint(index_view)

    db.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    if not os.path.exists("local.db"):
        with app.app_context():
            db.create_all()    
    app.run(debug=bool(os.getenv("DEBUG","False")))