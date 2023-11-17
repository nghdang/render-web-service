# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Blueprint, g, request, jsonify

import services_provider
from waiting import WaitingManager

blueprint = Blueprint("add", __name__, url_prefix="/")

@blueprint.route("/add", methods=["POST"])
def add_registrations():
    wait_mgr = services_provider.get_service(g, WaitingManager)
    assert wait_mgr is not None

    json_object = wait_mgr.add_registration(request.get_json())
    return jsonify(json_object)
