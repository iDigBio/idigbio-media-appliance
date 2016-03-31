from .config import SQLALCHEMY_DATABASE_URI
from .config import SQLALCHEMY_MIGRATE_REPO
from .app import db


def create_or_update_db():
    import os.path
    db.create_all()

if __name__ == '__main__':
    create_or_update_db()
