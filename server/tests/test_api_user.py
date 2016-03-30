from __future__ import absolute_import, print_function, division, unicode_literals

import os
import json
from flask import url_for

from .conftest import do_login


def test_user_api_login(api_login):
    assert "user_uuid" in api_login.json
    assert "auth_key" not in api_login.json


def test_user_api_login_twice(api_login, json_in_out, client):
    res = do_login(client, json_in_out)
    assert "user_uuid" in res.json
    assert "auth_key" not in res.json


def test_user_api_logout(api_login, json_in_out, client):
    res = client.delete(url_for('appuser_api.appuserapi'), headers=json_in_out)
    assert res.json == {}


def test_user_api_logout_login(api_login, json_in_out, client):
    res = client.delete(url_for('appuser_api.appuserapi'), headers=json_in_out)
    assert res.json == {}

    res = do_login(client, json_in_out)
    assert "user_uuid" in res.json
    assert "auth_key" not in res.json


def test_user_api_get(api_login, json_in_out, client):
    res = client.get(url_for('appuser_api.appuserapi'), headers=json_in_out)
    assert res.json.get("user_uuid") == "beefbeef-beef-beef-beef-beefbeefbeef"
    assert "auth_key" not in res.json
