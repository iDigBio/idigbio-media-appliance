from __future__ import absolute_import, print_function, division, unicode_literals

from ..app import db

from enum import Enum


class Media(db.Model):

    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)
    media_type = db.Column(db.Text)
    mime = db.Column(db.Text)
    path = db.Column(db.Text, nullable=False, unique=True)
    file_reference = db.Column(db.Text, nullable=False)
    props = db.Column(db.Text, default="{}")
    image_hash = db.Column(db.Text)
    status = db.Column(
        db.Enum(*["uploaded", "failed", "missing", "file_changed"]))
    status_date = db.Column(db.DateTime)
    status_detail = db.Column(db.Text)
    appuser_id = db.Column(db.Integer, db.ForeignKey(
        'appuser.id'), nullable=False)
    appuser = db.relationship("AppUser", backref="media")
