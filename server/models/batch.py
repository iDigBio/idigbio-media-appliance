from app import db

class Batch(db.Model):

    __tablename__ = "batches"

    id = db.Column(db.Integer,primary_key=True)
    csvfile=db.Column(db.String(255))