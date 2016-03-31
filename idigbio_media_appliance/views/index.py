from __future__ import absolute_import, print_function, division, unicode_literals

from flask import render_template, Blueprint

from ..models import AppUser

index_view = Blueprint('index', __name__)


@index_view.route('/')
def index():
    users = AppUser.query.all()

    return render_template('index.html', users=users)
