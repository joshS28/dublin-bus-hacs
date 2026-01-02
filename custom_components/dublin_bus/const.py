"""Constants for the Dublin Bus RTPI integration."""

DOMAIN = "dublin_bus"

CONF_STOP_IDS = "stop_ids"
CONF_ROUTE_FILTERS = "route_filters"

# TFI LTS API endpoints
LTS_BASE_URL = "https://api-lts.transportforireland.ie/lts/lts/v1/public"
API_LOOKUP = f"{LTS_BASE_URL}/locationOrServiceLookup"
API_DEPARTURES = f"{LTS_BASE_URL}/departures"

# Default values
DEFAULT_SCAN_INTERVAL = 30  # seconds
DEFAULT_NAME = "Dublin Bus"

# Attribution
ATTRIBUTION = "Data provided by Transport for Ireland"
