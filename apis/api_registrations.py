# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Blueprint, g, request, jsonify

import services_provider
from waiting import WaitingManager

blueprint = Blueprint("registrations", __name__, url_prefix="/")

@blueprint.route("/registrations", methods=["GET"])
def get_registrations():
    wait_mgr = services_provider.get_service(g, WaitingManager)
    assert wait_mgr is not None

    store_id = int(request.args.get("store_id"))
    is_completed = int(request.args.get("is_completed"))
    json_object = wait_mgr.get_registrations(store_id, is_completed)
    return jsonify(json_object)
