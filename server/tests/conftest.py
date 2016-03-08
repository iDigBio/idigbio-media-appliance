import pytest
import os

@pytest.fixture
def datadir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "testdata")

@pytest.fixture
def send_json():
    return [("Content-Type", "application/json")]

@pytest.fixture
def json_in_out(send_json, accept_json):
    return send_json + accept_json


@pytest.fixture
def app(request):
    os.environ["DATABASE_URL"] = "sqlite://"
    from app import init_routes, app as flask_app, db
    db.drop_all()
    db.create_all()
    db.session.commit()
    try:
        init_routes()
    except: # can only initialize apps once
        pass
    flask_app.debug = True

    return flask_app