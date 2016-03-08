from app import db

class Media(db.Model):

    __tablename__ = "media"

    id = db.Column(db.Integer,primary_key=True)
    media_type = db.Column(db.Text)
    mime = db.Column(db.Text)
    path = db.Column(db.Text, nullable=False)
    file_reference = db.Column(db.Text, nullable=False)
    image_hash = db.Column(db.Text)
    uploaded = db.Column(db.Boolean)
    uploaded_date = db.Column(db.DateTime)