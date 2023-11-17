# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

from shared_constants import TOTAL_REGISTRATIONS, TOTAL_WAITING_MINUTES, WAITING_MINUTES_PER_TEAM, \
    RegsTableHeader, StoreSettingsTableHeader
from server import app as application

####
# Test APIs
# /add
def test_api_add(phone_number, team_size):
    from server import wait_mgr

    registration = wait_mgr.add_registration({
        RegsTableHeader.REGISTRATION_ID: -1,
        RegsTableHeader.STORE_ID: 1,
        RegsTableHeader.WAITING_ORDER: -1,
        RegsTableHeader.PHONE_NUMBER: phone_number,
        RegsTableHeader.TEAM_SIZE: team_size,
        RegsTableHeader.TIMESTAMP: "",
        RegsTableHeader.STATUS: -1
    })
    print(json.dumps({
        RegsTableHeader.REGISTRATION_ID: registration.get_id(),
        RegsTableHeader.STORE_ID: registration.get_store_id(),
        RegsTableHeader.WAITING_ORDER: registration.get_waiting_order(),
        RegsTableHeader.PHONE_NUMBER: registration.get_phone_number(),
        RegsTableHeader.TEAM_SIZE: registration.get_team_size(),
        RegsTableHeader.TIMESTAMP: registration.get_timestamp(),
        RegsTableHeader.STATUS: registration.get_status()
    }, indent=4))

# /dashboard
def test_api_dashboard(store_id):
    from server import wait_mgr

    total_registrations, waiting_minutes_per_team = wait_mgr.get_dashboard(store_id)
    print(json.dumps({
        TOTAL_REGISTRATIONS: total_registrations,
        TOTAL_WAITING_MINUTES: total_registrations*waiting_minutes_per_team,
        WAITING_MINUTES_PER_TEAM: waiting_minutes_per_team
    }, indent=4))

# /registrations
def test_api_registrations(store_id):
    from server import wait_mgr

    registrations = wait_mgr.get_registrations(store_id)
    printable_registrations = []
    for registration in registrations.values():
        printable_registrations.append({
            RegsTableHeader.REGISTRATION_ID: registration.get_id(),
            RegsTableHeader.STORE_ID: registration.get_store_id(),
            RegsTableHeader.WAITING_ORDER: registration.get_waiting_order(),
            RegsTableHeader.PHONE_NUMBER: registration.get_phone_number(),
            RegsTableHeader.TEAM_SIZE: registration.get_team_size(),
            RegsTableHeader.TIMESTAMP: registration.get_timestamp(),
            RegsTableHeader.STATUS: registration.get_status()
        })
    print(json.dumps(printable_registrations, indent=4))

# /reset
def test_api_reset(store_id):
    from server import wait_mgr

    wait_mgr.reset_waiting_order(store_id)

# /status
def test_api_status(reg_id, store_id, reg_status):
    from server import wait_mgr

    json_object = {
        RegsTableHeader.REGISTRATION_ID: reg_id,
        RegsTableHeader.STORE_ID: store_id,
        RegsTableHeader.STATUS: reg_status
    }

    total_registrations, waiting_minutes_per_team = wait_mgr.change_registration_status(json_object)
    print(json.dumps({
        TOTAL_REGISTRATIONS: total_registrations,
        TOTAL_WAITING_MINUTES: total_registrations*waiting_minutes_per_team,
        WAITING_MINUTES_PER_TEAM: waiting_minutes_per_team
    }, indent=4))

# /change
def test_api_change(store_id, waiting_minutes_per_team):
    from server import wait_mgr

    json_object = {
        StoreSettingsTableHeader.WAITING_MINUTES_PER_TEAM: waiting_minutes_per_team
    }

    wait_mgr.change_waiting_minutes_per_team(store_id, json_object)

if __name__ == "__main__":
    application.run("0.0.0.0")
    # test_api_add("010-1234-5678", 2)
    # test_api_add("010-8765-4321", 4)
    # test_api_dashboard(1)
    # test_api_registrations(1)
    # test_api_reset(1)
    # test_api_status(1, 1, 1)
    # test_api_change(1, 5)
