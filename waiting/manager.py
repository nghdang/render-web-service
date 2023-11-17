# -*- coding: utf-8 -*-

from __future__ import absolute_import

from shared_constants import RegsTableHeader, StoreSettingsTableHeader

class WaitingManager:
    def __init__(self, wait_db_adapter, wait_factory):
        self.__wait_db_adapter = wait_db_adapter
        self.__wait_factory = wait_factory
        self.__stores = {}

    def __create_store(self, store_id):
        store = self.__wait_factory.create_store(store_id, self.__wait_db_adapter)
        store.init()
        self.__stores[store_id] = store
        return store

    def __get_store(self, store_id):
        store = self.__stores.get(store_id)
        if store is None:
            store = self.__create_store(store_id)
        return store

    def init_stores(self):
        self.__stores = {}
        for store_id in self.__wait_db_adapter.get_store_ids():
            self.__create_store(store_id)

    def get_dashboard(self, store_id):
        return self.__get_store(store_id).get_dashboard()

    def add_registration(self, json_object):
        registration = self.__wait_factory.create_registration()
        registration.fill_customer_info(json_object[RegsTableHeader.PHONE_NUMBER], json_object[RegsTableHeader.TEAM_SIZE])
        store_id = json_object[RegsTableHeader.STORE_ID]
        registration = self.__get_store(store_id).add_registration(registration)
        return {
            RegsTableHeader.REGISTRATION_ID: registration.get_id(),
            RegsTableHeader.STORE_ID: registration.get_store_id(),
            RegsTableHeader.WAITING_ORDER: registration.get_waiting_order(),
            RegsTableHeader.PHONE_NUMBER: registration.get_phone_number(),
            RegsTableHeader.TEAM_SIZE: registration.get_team_size(),
            RegsTableHeader.TIMESTAMP: registration.get_timestamp(),
            RegsTableHeader.STATUS: registration.get_status()
        }

    def get_registrations(self, store_id, is_completed):
        registrations = self.__get_store(store_id).get_registrations(is_completed)
        json_object = []
        for registration in registrations.values():
            json_object.append({
                RegsTableHeader.REGISTRATION_ID: registration.get_id(),
                RegsTableHeader.STORE_ID: registration.get_store_id(),
                RegsTableHeader.WAITING_ORDER: registration.get_waiting_order(),
                RegsTableHeader.PHONE_NUMBER: registration.get_phone_number(),
                RegsTableHeader.TEAM_SIZE: registration.get_team_size(),
                RegsTableHeader.TIMESTAMP: registration.get_timestamp(),
                RegsTableHeader.STATUS: registration.get_status()
            })
        return json_object

    def reset_waiting_order(self, store_id):
        self.__get_store(store_id).reset_waiting_order()

    def change_registration_status(self, json_object):
        reg_id = json_object[RegsTableHeader.REGISTRATION_ID]
        store_id = json_object[RegsTableHeader.STORE_ID]
        reg_status = json_object[RegsTableHeader.STATUS]
        return self.__get_store(store_id).change_registration_status(reg_id, reg_status)

    def change_waiting_minutes_per_team(self, store_id, json_object):
        waiting_minutes_per_team = json_object[StoreSettingsTableHeader.WAITING_MINUTES_PER_TEAM]
        return self.__get_store(store_id).change_waiting_minutes_per_team(waiting_minutes_per_team)
