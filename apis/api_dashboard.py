# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Blueprint, g, request, jsonify

from shared_constants import TOTAL_REGISTRATIONS, TOTAL_WAITING_MINUTES, WAITING_MINUTES_PER_TEAM
import services_provider
from waiting import WaitingManager

blueprint = Blueprint("dashboard", __name__, url_prefix="/")

@blueprint.route("/dashboard", methods=["GET"])
def get_dashboard():
    wait_mgr = services_provider.get_service(g, WaitingManager)
    assert wait_mgr is not None

    store_id = int(request.args.get("store_id"))
    total_registrations, waiting_minutes_per_team = wait_mgr.get_dashboard(store_id)
    return jsonify({
        TOTAL_REGISTRATIONS: total_registrations,
        TOTAL_WAITING_MINUTES: total_registrations*waiting_minutes_per_team,
        WAITING_MINUTES_PER_TEAM: waiting_minutes_per_team
    })
