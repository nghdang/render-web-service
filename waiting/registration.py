# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime

from shared_constants import RegStatus, TIMESTAMP_FORMAT

class WaitingRegistration:
    def __init__(self, reg_id):
        self.__reg_id = reg_id
        self.__store_id = -1
        self.__waiting_order = -1
        self.__phone_number = ""
        self.__team_size = -1
        self.__timestamp = datetime.datetime.now().isoformat(timespec="milliseconds")
        self.__status = RegStatus.REGISTERED

    def get_id(self):
        return self.__reg_id

    def get_store_id(self):
        return self.__store_id

    def get_waiting_order(self):
        return self.__waiting_order

    def get_phone_number(self):
        return self.__phone_number

    def get_team_size(self):
        return self.__team_size

    def get_timestamp(self):
        return self.__timestamp

    def get_status(self):
        return self.__status

    def fill_customer_info(self, phone_number, team_size):
        self.__phone_number = phone_number
        self.__team_size = team_size

    def fill_store_info(self, store_id, waiting_order):
        self.__store_id = store_id
        self.__waiting_order = waiting_order

    def parse_from_database(self, row):
        reg_id, store_id, waiting_order, phone_number, team_size, timestamp, status = row
        self.__reg_id = reg_id
        self.__store_id = store_id
        self.__waiting_order = waiting_order
        self.__phone_number = phone_number
        self.__team_size = team_size
        self.__timestamp = timestamp
        self.__status = status
