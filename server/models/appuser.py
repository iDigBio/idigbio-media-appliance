from __future__ import absolute_import, print_function, division, unicode_literals

from ..app import db


class AppUser(db.Model):

    __tablename__ = "appuser"

    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.Text, nullable=False, unique=True)
    user_alias = db.Column(db.Text, unique=True)
    auth_key = db.Column(db.Text, nullable=False)
    config = db.Column(db.Text, default="{}")
    login_date = db.Column(db.DateTime)
