from app import db


class AppUser(db.Model):

    __tablename__ = "appuser"

    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.Text, nullable=False, unique=True)
    auth_key = db.Column(db.Text, nullable=False)
    config = db.Column(db.Text, default="{}")
    login_date = db.Column(db.DateTime)
