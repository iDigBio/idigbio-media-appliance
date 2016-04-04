from __future__ import absolute_import, print_function, division, unicode_literals

import os
import webbrowser

from .app import init_routes, create_or_update_db, app


def main():
    dbg = "True" == os.getenv("DEBUG", "False")
    init_routes()
    create_or_update_db()
    webbrowser.open("http://localhost:5000")
    if dbg:
        # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        app.run()
    else:
        app.run()

if __name__ == '__main__':
    main()
