from flask import Blueprint
from flask_restful import Api, Resource
from models import Batch

batch_api = Api(Blueprint("batch_api", __name__))

@batch_api.resource("/batches")
class BatchesAPI(Resource):

    @staticmethod
    def get():
        return { "batches": [
            {
                "id": batch.id,
                "csvfile": batch.csvfile
            } for batch in Batch.query
        ]}

    @staticmethod
    def post():
        from app import db

        batch = Batch()
        batch.csvfile = request.json.csvfile
        db.session.add(batch)
        db.session.commit()
 
        return {
            "id": batch.id,
            "csvfile": batch.csvfile
        }

@batch_api.resource("/batch/<int:batch_id>")
class BatchAPI(Resource):

    @staticmethod
    def get(batch_id):
        from app import db

        batch = Batch.query.get_or_404(batch_id)

        return {
            "id": batch.id,
            "csvfile": batch.csvfile
        }