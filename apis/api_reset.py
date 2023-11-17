# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Blueprint, g, request, jsonify

import services_provider
from waiting import WaitingManager

blueprint = Blueprint("reset", __name__, url_prefix="/")

@blueprint.route("/reset", methods=["PUT"])
def reset_waiting_order():
    wait_mgr = services_provider.get_service(g, WaitingManager)
    assert wait_mgr is not None

    store_id = int(request.args.get("store_id"))
    wait_mgr.reset_waiting_order(store_id)
    return jsonify({})
