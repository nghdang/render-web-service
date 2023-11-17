# -*- coding: utf-8 -*-

from __future__ import absolute_import

class DbTableSetting:
    def __init__(self):
        self.name = ""
        self.headers = {}
        self.primary_key = ""

    def parse(self, setting):
        self.name = setting["NAME"]
        for header_name, header_type in setting["HEADERS"].items():
            self.headers[header_name] = header_type
        self.primary_key = setting["PRIMARY_KEY"]
