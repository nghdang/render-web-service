# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Blueprint, g, request, jsonify

from shared_constants import TOTAL_REGISTRATIONS, TOTAL_WAITING_MINUTES, WAITING_MINUTES_PER_TEAM
import services_provider
from waiting import WaitingManager

blueprint = Blueprint("status", __name__, url_prefix="/")

@blueprint.route("/status", methods=["PUT"])
def change_registration_status():
    wait_mgr = services_provider.get_service(g, WaitingManager)
    assert wait_mgr is not None

    total_registrations, waiting_minutes_per_team = wait_mgr.change_registration_status(request.get_json())
    return jsonify({
        TOTAL_REGISTRATIONS: total_registrations,
        TOTAL_WAITING_MINUTES: total_registrations*waiting_minutes_per_team,
        WAITING_MINUTES_PER_TEAM: waiting_minutes_per_team
    })
