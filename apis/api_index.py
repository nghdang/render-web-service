# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Blueprint

blueprint = Blueprint("index", __name__, url_prefix="/")

@blueprint.route("/")
def index():
    return "<p>Hello World!</p>"
