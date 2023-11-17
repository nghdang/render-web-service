# -*- coding: utf-8 -*-

from __future__ import absolute_import


def has_service(app_globals, serviceClass):
    serviceId = str(serviceClass.__name__)
    return hasattr(app_globals, serviceId)

def get_service(app_globals, serviceClass):
    serviceId = str(serviceClass.__name__)
    service = None
    if hasattr(app_globals, serviceId):
        service = getattr(app_globals, serviceId)
    return service

def register_service(app_globals, service, replace=False):
    status = False
    serviceId = str(service.__class__.__name__)
    print(f"[ServicesProvider] Register service {serviceId}")
    if replace or not hasattr(app_globals, serviceId):
        setattr(app_globals, serviceId, service)
        status = True
    return status

