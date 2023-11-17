# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys
import pymysql

class DbClient:

    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def connect(self, setting, name):
        try:
            self.__connection = pymysql.connect(
                host=setting.host,
                port=setting.port,
                user=setting.username,
                password=setting.password,
                database=name
            )
            self.__cursor = self.__connection.cursor()
        except pymysql.Error as e:
            print(f"Error connecting to Database http://{setting.username}:****@{setting.host}:{setting.port}/{name}: {e}")
            sys.exit(-1)

    def disconnect(self):
        if self.__connection is not None:
            self.__connection.close()

    def exec_query(self, query):
        rows = []
        try:
            self.__cursor.execute(query)
            print(f"Success to execute query: {query}")

            for row in self.__cursor:
                rows.append(row)
        except pymysql.Error as e:
            print(f"Error execute query: {query}\n    {e}")
        return rows

    def exec_query_and_commit(self, query):
        rows = self.exec_query(query)
        self.__connection.commit()
        return rows
