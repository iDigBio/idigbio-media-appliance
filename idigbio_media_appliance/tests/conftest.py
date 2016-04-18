from __future__ import absolute_import, print_function, division, unicode_literals

import pytest
import os
import json

from flask import url_for


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
    from ..app import init_routes, app as flask_app, db
    db.drop_all()
    db.create_all()
    db.session.commit()
    try:
        init_routes()
    except:  # can only initialize apps once
        pass
    flask_app.debug = True

    return flask_app


def do_login(client, json_in_out):
    res = client.post(url_for('appuser_api.appuserapi'), data=json.dumps({
        "user_uuid": "beefbeef-beef-beef-beef-beefbeefbeef",
        "auth_key": "1ff708ecbeca259d8bc852798022cf1cec7bc71d"
    }), headers=json_in_out)
    return res


@pytest.fixture
def api_login(client, json_in_out):
    return do_login(client, json_in_out)
