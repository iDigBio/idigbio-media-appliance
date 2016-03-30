from __future__ import absolute_import, print_function, division, unicode_literals

import os

from .app import init_routes, create_or_update_db, app

if __name__ == '__main__':
    dbg = "True" == os.getenv("DEBUG", "False")
    init_routes()
    create_or_update_db()
    if dbg:
        # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        app.run()
    else:
        app.run()
