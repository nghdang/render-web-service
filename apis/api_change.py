# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Blueprint, g, request, jsonify

import services_provider
from waiting import WaitingManager

blueprint = Blueprint("change", __name__, url_prefix="/")

@blueprint.route("/change", methods=["PUT"])
def change_waiting_minutes_per_team():
    wait_mgr = services_provider.get_service(g, WaitingManager)
    assert wait_mgr is not None

    store_id = int(request.args.get("store_id"))
    wait_mgr.change_waiting_minutes_per_team(store_id, request.get_json())
    return jsonify({})
