# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .database import DbDatabase
from .client import DbClient
from .table import DbTable
from .header import DbHeader

class DbFactory:

    def create_database(self):
        return DbDatabase(self)

    def create_client(self):
        return DbClient()

    def create_table(self, client):
        return DbTable(self, client)

    def create_header(self, name, type):
        return DbHeader(name, type)
