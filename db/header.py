# -*- coding: utf-8 -*-

from __future__ import absolute_import

class DbHeader:
    def __init__(self, name, type):
        self.__name = name
        self.__type = type
        self.__is_primary_key = False

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_is_primary_key(self):
        return self.__is_primary_key

    def set_primary_key(self):
        self.__is_primary_key = True
