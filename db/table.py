# -*- coding: utf-8 -*-

from __future__ import absolute_import


class DbTable:
    def __init__(self, factory, client):
        self.__factory = factory
        self.__name = ""
        self.__client = client
        self.__headers = {}

    def get_name(self):
        return self.__name

    def get_headers(self):
        return list(self.__headers.keys())

    def init(self, setting):
        self.__name = setting.name
        for header_name, header_type in setting.headers.items():
            header = self.__factory.create_header(header_name, header_type)
            self.__headers[header.get_name()] = header
        self.__headers[setting.primary_key].set_primary_key()

    def exec_query(self, query):
        return self.__client.exec_query_and_commit(query)

    def remove(self):
        query = f"DROP TABLE IF EXISTS {self.__name}"
        self.__client.exec_query_and_commit(query)

    def create(self, replace=False):
        if replace:
            query = f"DROP TABLE IF EXISTS {self.__name}"
            self.__client.exec_query(query)

        headers_query = []
        for header in self.__headers.values():
            if header.get_is_primary_key():
                headers_query.append(f"{header.get_name()} {header.get_type()} PRIMARY KEY")
            else:
                headers_query.append(f"{header.get_name()} {header.get_type()}")

        query = f"CREATE TABLE IF NOT EXISTS {self.__name} ({','.join(headers_query)})"
        self.__client.exec_query_and_commit(query)

    def add_row(self, header_values):
        if len(header_values) != len(self.__headers):
            print(f"ERROR: [{self.__name}] Cannot add row because of missing data")
        else:
            header_values_str = "','".join([str(value) for value in header_values])
            header_names_str = ",".join(list(self.__headers.keys()))
            query = f"INSERT INTO {self.__name} ({header_names_str}) VALUES ('{header_values_str}')"
            self.__client.exec_query_and_commit(query)

    def get_rows(self, header_names, conditions=None):
        header_names_str = ",".join(header_names)

        if conditions is None:
            query = f"SELECT {header_names_str} FROM {self.__name}"
        else:
            condition_strlist = []
            for header_name, header_value in conditions.items():
                condition_strlist.append(f"{header_name}='{header_value}'")
            condition_str = " AND ".join(condition_strlist)

            query = f"SELECT {header_names_str} FROM {self.__name} WHERE {condition_str}"
        return self.__client.exec_query(query)

    def update_columns(self, header_values, conditions):
        header_query_strlist = []
        for header_name, header_value in header_values.items():
            header_query_strlist.append(f"{header_name}='{header_value}'")
        header_query_str = ",".join(header_query_strlist)

        condition_strlist = []
        for header_name, header_value in conditions.items():
            condition_strlist.append(f"{header_name}='{header_value}'")
        condition_str = " AND ".join(condition_strlist)

        query = f"UPDATE {self.__name} SET {header_query_str} WHERE {condition_str}"
        self.__client.exec_query_and_commit(query)
