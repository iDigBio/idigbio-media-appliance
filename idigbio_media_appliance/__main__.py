from __future__ import absolute_import, print_function, division, unicode_literals

import os
import sys
import webbrowser
import subprocess
import logging
import multiprocessing


def main():
    # This probably means that OSX will only work on python 3.5 and higher
    if sys.version_info >= (3,4):
        multiprocessing.set_start_method('spawn')

    dbg = "True" == os.getenv("DEBUG", "False")

    try:
        subprocess.run(["conda", "install", "-y", "idigbio-media-appliance"])
    except:
        logging.exception("Update Error")

    from .app import init_routes, create_or_update_db, app
    init_routes()
    create_or_update_db()
    webbrowser.open("http://localhost:5000")
    if dbg:
        # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        app.run(debug=True)
    else:
        app.run()

if __name__ == '__main__':
    main()
