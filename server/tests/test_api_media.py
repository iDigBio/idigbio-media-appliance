from __future__ import absolute_import, print_function, division, unicode_literals

import os
import json
from flask import url_for


def test_media_api_list(api_login, json_in_out, client):
    res = client.get(url_for('media_api.mediaapi'), headers=json_in_out)
    assert "count" in res.json
    assert "media" in res.json


def test_media_api_post(api_login, json_in_out, client, datadir):
    image_path = os.path.join(datadir, "images/image1.jpg")
    image_ref = "TESTDATA:" + image_path.split("/")[-1]
    res = client.post(url_for('media_api.mediaapi'), data=json.dumps({
        "path": image_path,
        "file_reference": "TESTDATA:" + image_path.split("/")[-1]
    }), headers=json_in_out)
    assert res.json.get("id") is not None
    assert res.json.get("path") == image_path
    assert res.json.get("file_reference") == image_ref


def test_media_api_post_nologin(json_in_out, client, datadir):
    image_path = os.path.join(datadir, "images/image1.jpg")
    image_ref = "TESTDATA:" + image_path.split("/")[-1]
    res = client.post(url_for('media_api.mediaapi'), data=json.dumps({
        "path": image_path,
        "file_reference": "TESTDATA:" + image_path.split("/")[-1]
    }), headers=json_in_out)
    assert res.status_code == 401


def test_media_api_post_get(api_login, json_in_out, client, datadir):
    image_path = os.path.join(datadir, "images/image1.jpg")
    image_ref = "TESTDATA:" + image_path.split("/")[-1]
    res = client.post(url_for('media_api.mediaapi'), data=json.dumps({
        "path": image_path,
        "file_reference": "TESTDATA:" + image_path.split("/")[-1]
    }), headers=json_in_out)
    assert res.json.get("id") is not None
    assert res.json.get("path") == image_path
    assert res.json.get("file_reference") == image_ref

    get_res = client.get(url_for('media_api.mediaapi', id=res.json.get("id")))

    assert res.json.get("id") == res.json.get("id")
    assert res.json.get("path") == res.json.get("path")
    assert res.json.get("file_reference") == res.json.get("file_reference")
