# -*- coding: utf-8 -*-

from __future__ import absolute_import

from shared_constants import WATING_DATABASE_NAME, REGISTRATIONS_TABLE_NAME, STORE_SETTINGS_TABLE_NAME, \
    RegsTableHeader, StoreSettingsTableHeader

class WaitingDbAdapter:
    def __init__(self, dbManager) -> None:
        self.__dbManager = dbManager
        self.__wait_factory = None

        self.__waiting_db = self.__dbManager.get_database(WATING_DATABASE_NAME)
        assert self.__waiting_db is not None

        self.__registrations_tb = self.__waiting_db.get_table(REGISTRATIONS_TABLE_NAME)
        assert self.__registrations_tb is not None

        self.__store_settings_tb = self.__waiting_db.get_table(STORE_SETTINGS_TABLE_NAME)
        assert self.__store_settings_tb is not None

    def set_wait_factory(self, wait_factory):
        self.__wait_factory = wait_factory

    def get_last_reg_id(self):
        query = f"SELECT {RegsTableHeader.REGISTRATION_ID} FROM {REGISTRATIONS_TABLE_NAME} " \
                f"ORDER BY {RegsTableHeader.REGISTRATION_ID} DESC LIMIT 1"
        rows = self.__registrations_tb.exec_query(query)
        last_reg_id = 0
        if rows and rows[0]:
            last_reg_id = rows[0][0]
        return last_reg_id + 1


    def get_store_ids(self):
        header_names = [StoreSettingsTableHeader.STORE_ID]
        rows = self.__store_settings_tb.get_rows(header_names)
        store_ids = []
        for row in rows:
            store_ids.append(row[0])
        return store_ids

    def add_registration(self, registration):
        self.__registrations_tb.add_row([
            registration.get_id(),
            registration.get_store_id(),
            registration.get_waiting_order(),
            registration.get_phone_number(),
            registration.get_team_size(),
            registration.get_timestamp(),
            registration.get_status()
        ])

    def get_registrations(self, store_id, reg_status=None):
        header_names = [
            RegsTableHeader.REGISTRATION_ID,
            RegsTableHeader.STORE_ID,
            RegsTableHeader.WAITING_ORDER,
            RegsTableHeader.PHONE_NUMBER,
            RegsTableHeader.TEAM_SIZE,
            RegsTableHeader.TIMESTAMP,
            RegsTableHeader.STATUS
        ]
        conditions = {
            RegsTableHeader.STORE_ID: store_id,
            RegsTableHeader.STATUS: reg_status
        }
        rows = self.__registrations_tb.get_rows(header_names, conditions)
        registrations = []
        for row in rows:
            registration = self.__wait_factory.create_registration_from_database(row)
            registrations.append(registration)
        return registrations

    def get_last_waiting_order(self, store_id):
        query = f"SELECT {RegsTableHeader.REGISTRATION_ID}, {RegsTableHeader.WAITING_ORDER} " \
                f"FROM {REGISTRATIONS_TABLE_NAME} WHERE {RegsTableHeader.STORE_ID}='{store_id}' " \
                f"ORDER BY {RegsTableHeader.REGISTRATION_ID} DESC LIMIT 1"
        rows = self.__registrations_tb.exec_query(query)
        last_waiting_order = 0
        if rows and rows[0]:
            last_waiting_order = rows[0][1]
        return last_waiting_order + 1

    def get_waiting_minutes_per_team(self, store_id):
        header_names = [StoreSettingsTableHeader.WAITING_MINUTES_PER_TEAM]
        conditions = {StoreSettingsTableHeader.STORE_ID: store_id}
        rows = self.__store_settings_tb.get_rows(header_names, conditions)
        if rows:
            return rows[0][0]
        else:
            return -1

    def change_registration_status(self, reg_id, reg_status):
        header_values = {RegsTableHeader.STATUS: reg_status}
        conditions = {RegsTableHeader.REGISTRATION_ID: reg_id}
        self.__registrations_tb.update_columns(header_values, conditions)

    def add_store(self, store_id, waiting_minutes_per_team):
        self.__store_settings_tb.add_row([store_id, waiting_minutes_per_team])

    def change_waiting_minutes_per_team(self, store_id, waiting_minutes_per_team):
        header_values = {StoreSettingsTableHeader.WAITING_MINUTES_PER_TEAM: waiting_minutes_per_team}
        conditions = {StoreSettingsTableHeader.STORE_ID: store_id}
        self.__store_settings_tb.update_columns(header_values, conditions)
