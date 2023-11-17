# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .db_table_setting import DbTableSetting

class DbDatabaseSetting:
    def __init__(self):
        self.name = ""
        self.tables = []

    def parse(self, setting):
        self.name = setting["NAME"]
        for table_setting in setting["TABLES"]:
            table = DbTableSetting()
            table.parse(table_setting)
            self.tables.append(table)
