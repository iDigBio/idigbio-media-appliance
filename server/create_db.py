from migrate.versioning import api
from migrate.exceptions import DatabaseAlreadyControlledError
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db


def create_or_update_db():
    try:
        import os.path
        db.create_all()
        if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
            api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)  # noqa
        else:
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,  # noqa
                                api.version(SQLALCHEMY_MIGRATE_REPO)
                                )
    except DatabaseAlreadyControlledError:
        pass

if __name__ == '__main__':
    create_or_update_db()
