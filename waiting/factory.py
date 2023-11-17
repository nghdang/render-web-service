# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .registration import WaitingRegistration
from .store import WaitingStore

class WaitingFactory:

    def __init__(self, reg_id) :
        self.__reg_id_generator = reg_id

    def create_store(self, store_id, db_manager):
        return WaitingStore(store_id, db_manager)

    def create_registration(self):
        registration = WaitingRegistration(self.__reg_id_generator)
        self.__reg_id_generator += 1
        return registration

    def create_registration_from_database(self, row):
        registration = WaitingRegistration(0)
        registration.parse_from_database(row)
        return registration
