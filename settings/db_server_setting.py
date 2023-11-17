# -*- coding: utf-8 -*-

from __future__ import absolute_import

class DbServerSetting:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.username = "root"
        self.password = "root"

    def parse(self, setting):
        self.host = setting["HOST"]
        self.port = setting["PORT"]
        self.username = setting["USERNAME"]
        self.password = setting["PASSWORD"]
