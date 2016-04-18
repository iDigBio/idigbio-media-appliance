from __future__ import absolute_import, print_function, division, unicode_literals

from ..lib.dir_handling import guid_mode

import uuid
import re
import os


def test_uuid(datadir):
    g = guid_mode["uuid"](datadir + "/images/image1.jpg")
    u = uuid.UUID(g)
    assert u is not None


def test_hash(datadir):
    g = guid_mode["hash"](datadir + "/images/image1.jpg")
    assert g == "b1b818a7824ff6822bffa6ea625ec147"


def test_prefix_fullpath(datadir):
    prefix = "test:"
    path = datadir + "/images/image1.jpg"
    params = (prefix + "\\1", path)

    g = guid_mode["fullpath"](*params)
    assert g == prefix + path


def test_prefix_filename(datadir):
    prefix = "test:"
    path = datadir + "/images/image1.jpg"
    params = (prefix + "\\1", path)

    g = guid_mode["filename"](*params)
    assert g == prefix + os.path.basename(path)
