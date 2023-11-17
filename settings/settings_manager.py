# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import json

from shared_constants import SETTING_JSON_NAME
from .db_server_setting import DbServerSetting
from .db_database_setting import DbDatabaseSetting

class SettingsManager:
    SETTINGS_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", SETTING_JSON_NAME)

    def __init__(self):
        self.database_server = DbServerSetting()
        self.databases = []

    def parse(self):
        with open(self.SETTINGS_JSON_PATH, "r", encoding="utf-8") as fh:
            setting = json.load(fh)
            self.database_server.parse(setting["DATABASE_SERVER"])
            for database_setting in setting["DATABASES"]:
                database = DbDatabaseSetting()
                database.parse(database_setting)
                self.databases.append(database)
