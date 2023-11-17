# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Flask, g

from settings import SettingsManager
from db import DbManager, DbFactory
from waiting import WaitingManager, WaitingDbAdapter, WaitingFactory
import apis
import services_provider

# Init app dependencies
print("[Main] Init SettingsManager")
setting_mgr = SettingsManager()
setting_mgr.parse()

print("[Main] Init DatabaseManager")
db_factory = DbFactory()
db_mgr = DbManager(db_factory)
db_mgr.init(setting_mgr.database_server, setting_mgr.databases)

print("[Main] Init WaitingManager")
wait_db_adapter = WaitingDbAdapter(db_mgr)
wait_factory = WaitingFactory(wait_db_adapter.get_last_reg_id())
wait_db_adapter.set_wait_factory(wait_factory)
wait_mgr = WaitingManager(wait_db_adapter, wait_factory)
wait_mgr.init_stores()

# Init app
print("[Main] Init Application")
app = Flask(__name__)

for blueprint in apis.blueprints:
    print(f"[Main] Register blueprint {blueprint.name}")
    app.register_blueprint(blueprint)

@app.before_request
def before_first_request():
    print("[API] Register WaitingManager")
    services_provider.register_service(g, wait_mgr)
