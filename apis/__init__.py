from .api_index import blueprint as blueprint_index
from .api_add import blueprint as blueprint_add
from .api_dashboard import blueprint as blueprint_dashboard
from .api_registrations import blueprint as blueprint_registrations
from .api_reset import blueprint as blueprint_reset
from .api_status import blueprint as blueprint_status
from .api_change import blueprint as blueprint_change

blueprints = [
    blueprint_index,
    blueprint_add,
    blueprint_dashboard,
    blueprint_registrations,
    blueprint_reset,
    blueprint_status,
    blueprint_change
]
