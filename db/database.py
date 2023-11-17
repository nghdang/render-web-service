# -*- coding: utf-8 -*-

from __future__ import absolute_import

class DbDatabase:
    def __init__(self, factory):
        self.__factory = factory
        self.__name = ""
        self.__client = self.__factory.create_client()
        self.__tables = {}

    def init(self, server_setting, database_setting):
        self.__client.connect(server_setting, database_setting.name)

        self.__name = database_setting.name
        for table_setting in database_setting.tables:
            table = self.__factory.create_table(self.__client)
            table.init(table_setting)
            table.create()
            self.__tables[table.get_name()] = table

    def get_name(self):
        return self.__name

    def get_table(self, name):
        return self.__tables.get(name)
