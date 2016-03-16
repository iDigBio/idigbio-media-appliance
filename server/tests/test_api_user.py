import os
import json
from flask import url_for


def test_user_api_login(json_in_out, client):
    res = client.post(url_for('appuser_api.appuserapi'), data=json.dumps({
        "user_uuid": "beefbeef-beef-beef-beef-beefbeefbeef",
        "auth_key": "1ff708ecbeca259d8bc852798022cf1cec7bc71d"
    }), headers=json_in_out)
    assert "user_uuid" in res.json
    assert "auth_key" not in res.json


def test_user_api_login_twice(json_in_out, client):
    res = client.post(url_for('appuser_api.appuserapi'), data=json.dumps({
        "user_uuid": "beefbeef-beef-beef-beef-beefbeefbeef",
        "auth_key": "1ff708ecbeca259d8bc852798022cf1cec7bc71d"
    }), headers=json_in_out)
    assert "user_uuid" in res.json
    assert "auth_key" not in res.json

    res = client.post(url_for('appuser_api.appuserapi'), data=json.dumps({
        "user_uuid": "beefbeef-beef-beef-beef-beefbeefbeef",
        "auth_key": "1ff708ecbeca259d8bc852798022cf1cec7bc71d"
    }), headers=json_in_out)
    assert "user_uuid" in res.json
    assert "auth_key" not in res.json


def test_user_api_logout(json_in_out, client):
    res = client.post(url_for('appuser_api.appuserapi'), data=json.dumps({
        "user_uuid": "beefbeef-beef-beef-beef-beefbeefbeef",
        "auth_key": "1ff708ecbeca259d8bc852798022cf1cec7bc71d"
    }), headers=json_in_out)
    assert "user_uuid" in res.json
    assert "auth_key" not in res.json

    res = client.delete(url_for('appuser_api.appuserapi'), headers=json_in_out)
    assert res.json == {}


def test_user_api_logout_login(json_in_out, client):
    res = client.post(url_for('appuser_api.appuserapi'), data=json.dumps({
        "user_uuid": "beefbeef-beef-beef-beef-beefbeefbeef",
        "auth_key": "1ff708ecbeca259d8bc852798022cf1cec7bc71d"
    }), headers=json_in_out)
    assert "user_uuid" in res.json
    assert "auth_key" not in res.json

    res = client.delete(url_for('appuser_api.appuserapi'), headers=json_in_out)
    assert res.json == {}

    res = client.post(url_for('appuser_api.appuserapi'), data=json.dumps({
        "user_uuid": "beefbeef-beef-beef-beef-beefbeefbeef",
        "auth_key": "1ff708ecbeca259d8bc852798022cf1cec7bc71d"
    }), headers=json_in_out)
    assert "user_uuid" in res.json
    assert "auth_key" not in res.json


def test_user_api_get(json_in_out, client):
    res = client.post(url_for('appuser_api.appuserapi'), data=json.dumps({
        "user_uuid": "beefbeef-beef-beef-beef-beefbeefbeef",
        "auth_key": "1ff708ecbeca259d8bc852798022cf1cec7bc71d"
    }), headers=json_in_out)
    assert "user_uuid" in res.json
    assert "auth_key" not in res.json

    res = client.get(url_for('appuser_api.appuserapi'), headers=json_in_out)
    assert res.json.get("user_uuid") == "beefbeef-beef-beef-beef-beefbeefbeef"
    assert "auth_key" not in res.json
