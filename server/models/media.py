from app import db

class Media(db.Model):

    __tablename__ = "media"

    id = db.Column(db.Integer,primary_key=True)
    media_type = db.Column(db.Text)
    mime = db.Column(db.Text)
    path = db.Column(db.Text, nullable=False, unique=True)
    file_reference = db.Column(db.Text, nullable=False)
    image_hash = db.Column(db.Text)
    uploaded = db.Column(db.Boolean, default=False, nullable=False)
    uploaded_date = db.Column(db.DateTime)