# -*- coding: utf-8 -*-

from __future__ import absolute_import

class DbManager:
    def __init__(self, factory) -> None:
        self.factory = factory
        self.databases = {}

    def init(self, server_setting, database_settings) -> None:
        for database_setting in database_settings:
            database = self.factory.create_database()
            database.init(server_setting, database_setting)
            self.databases[database.get_name()] = database

    def get_database(self, name):
        return self.databases.get(name)
