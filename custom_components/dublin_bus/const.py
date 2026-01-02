"""Constants for the Dublin Bus RTPI integration."""

DOMAIN = "dublin_bus"

CONF_STOP_IDS = "stop_ids"
CONF_ROUTE_FILTERS = "route_filters"

# NTA GTFS-R API endpoints
API_BASE_URL = "https://api.nationaltransport.ie/gtfsr/v2"
API_TRIP_UPDATES = f"{API_BASE_URL}/TripUpdates"

# Default values
DEFAULT_SCAN_INTERVAL = 30  # seconds
DEFAULT_NAME = "Dublin Bus"

# Attribution
ATTRIBUTION = "Data provided by National Transport Authority"
