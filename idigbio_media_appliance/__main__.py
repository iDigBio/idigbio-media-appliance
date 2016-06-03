from __future__ import absolute_import, print_function, division, unicode_literals

import os
import webbrowser
import subprocess
import logging



def main():
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
