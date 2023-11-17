# -*- coding: utf-8 -*-

from __future__ import absolute_import

from shared_constants import RegStatus, INITIAL_WAITING_ORDER, INITIAL_WAITING_TIME_PER_TEAM

class WaitingStore:
    def __init__(self, store_id, db_adapter):
        self.__store_id = store_id
        self.__db_adapter = db_adapter

        self.__waiting_order = INITIAL_WAITING_ORDER
        self.__waiting_minutes_per_team = INITIAL_WAITING_TIME_PER_TEAM
        self.__registrations = {}

    def init(self):
        registrations = self.__db_adapter.get_registrations(self.__store_id, RegStatus.REGISTERED)
        for registration in registrations:
            self.__registrations[registration.get_id()] = registration

        self.__waiting_order = self.__db_adapter.get_last_waiting_order(self.__store_id)
        self.__waiting_minutes_per_team = self.__db_adapter.get_waiting_minutes_per_team(self.__store_id)
        if self.__waiting_minutes_per_team < 0:
            self.__waiting_minutes_per_team = INITIAL_WAITING_TIME_PER_TEAM
            self.__db_adapter.add_store(self.__store_id, self.__waiting_minutes_per_team)

    def get_registrations(self, is_completed):
        registrations = {}
        if is_completed:
            entered_regs =  self.__db_adapter.get_registrations(self.__store_id, RegStatus.ENTERED)
            cancelled_regs =  self.__db_adapter.get_registrations(self.__store_id, RegStatus.CANCELLED)
            not_entered_regs =  self.__db_adapter.get_registrations(self.__store_id, RegStatus.NOT_ENTERED)
            for registration in entered_regs + cancelled_regs + not_entered_regs:
                registrations[registration.get_id()] = registration
        else:
            registrations = self.__registrations
        return registrations

    def get_dashboard(self):
        return (len(list(self.__registrations.keys())), self.__waiting_minutes_per_team)

    def add_registration(self, registration):
        registration.fill_store_info(self.__store_id, self.__waiting_order)
        self.__registrations[registration.get_id()] = registration
        self.__db_adapter.add_registration(registration)
        self.__waiting_order += 1
        return registration

    def reset_waiting_order(self):
        self.__waiting_order = INITIAL_WAITING_ORDER

    def change_registration_status(self, reg_id, reg_status):
        self.__db_adapter.change_registration_status(reg_id, reg_status)
        del self.__registrations[reg_id]
        return self.get_dashboard()

    def change_waiting_minutes_per_team(self, waiting_minutes_per_team):
        self.__waiting_minutes_per_team = waiting_minutes_per_team
        self.__db_adapter.change_waiting_minutes_per_team(self.__store_id, self.__waiting_minutes_per_team)
