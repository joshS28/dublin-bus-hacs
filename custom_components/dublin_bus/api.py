"""API client for Dublin Bus RTPI."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import requests
from google.transit import gtfs_realtime_pb2

from .const import API_TRIP_UPDATES

_LOGGER = logging.getLogger(__name__)


class DublinBusAPI:
    """API client for Dublin Bus real-time information."""

    def __init__(
        self,
        api_keys: list[str],
        stop_ids: list[str],
        route_filters: list[str] | None = None,
    ) -> None:
        """Initialize the API client."""
        self.api_keys = api_keys
        self.current_key_index = 0
        self.stop_ids = stop_ids
        self.route_filters = route_filters or []
        self.session = requests.Session()
        self._update_headers()

    def _update_headers(self) -> None:
        """Update session headers with current API key."""
        self.session.headers.update(
            {
                "x-api-key": self.api_keys[self.current_key_index],
                "Cache-Control": "no-cache",
            }
        )

    def test_connection(self) -> bool:
        """Test the API connection."""
        for _ in range(len(self.api_keys)):
            try:
                response = self.session.get(API_TRIP_UPDATES, timeout=10)
                response.raise_for_status()
                return True
            except Exception as err:
                _LOGGER.warning("Key %s failed: %s. Trying next key.", self.current_key_index, err)
                self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                self._update_headers()
        
        raise Exception("All API keys failed connection test")

    def get_stop_data(self) -> dict[str, Any]:
        """Fetch real-time data for configured stops."""
        for _ in range(len(self.api_keys)):
            try:
                response = self.session.get(API_TRIP_UPDATES, timeout=10)
                response.raise_for_status()

                # Parse GTFS-Realtime protobuf data
                feed = gtfs_realtime_pb2.FeedMessage()
                feed.ParseFromString(response.content)

                # Process data for each stop
                stops_data = {}
                for stop_id in self.stop_ids:
                    stops_data[stop_id] = self._process_stop_data(feed, stop_id)

                return stops_data

            except Exception as err:
                _LOGGER.error("Error with key %s: %s. Rotating key.", self.current_key_index, err)
                self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                self._update_headers()
        
        raise Exception("All API keys failed to fetch data")

    def _process_stop_data(
        self, feed: gtfs_realtime_pb2.FeedMessage, stop_id: str
    ) -> dict[str, Any]:
        """Process GTFS-R data for a specific stop."""
        arrivals = []

        for entity in feed.entity:
            if not entity.HasField("trip_update"):
                continue

            trip_update = entity.trip_update
            trip = trip_update.trip

            # Get route number
            route_id = trip.route_id if trip.HasField("route_id") else "Unknown"

            # Apply route filter if configured
            if self.route_filters and route_id not in self.route_filters:
                continue

            # Process stop time updates
            for stop_time_update in trip_update.stop_time_update:
                # Flexible matching: match if IDs are identical OR if the feed ID ends with the user's numeric ID
                feed_stop_id = stop_time_update.stop_id
                is_match = False
                
                if feed_stop_id == stop_id:
                    is_match = True
                elif stop_id.isdigit() and feed_stop_id.endswith(stop_id):
                    # Many NTA IDs are like 8220DB001192 for stop 1192
                    is_match = True
                elif stop_id.isdigit() and stop_id in feed_stop_id:
                    is_match = True

                if is_match:
                    arrival_time = None
                    if stop_time_update.HasField("arrival"):
                        arrival_time = stop_time_update.arrival.time
                    elif stop_time_update.HasField("departure"):
                        arrival_time = stop_time_update.departure.time

                    if arrival_time:
                        # Get trip headsign (destination)
                        destination = (
                            trip.trip_headsign
                            if trip.HasField("trip_headsign")
                            else "Unknown"
                        )
                        
                        # Strip platform info from destination if present (e.g. "Destination - Platform 1")
                        if " - " in destination:
                            destination = destination.split(" - ")[0]

                        # Calculate minutes until arrival
                        now = datetime.now(timezone.utc).timestamp()
                        minutes_until = int((arrival_time - now) / 60)

                        # Only include future arrivals
                        if minutes_until >= -1:
                            arrivals.append(
                                {
                                    "route": route_id,
                                    "destination": destination,
                                    "arrival_timestamp": arrival_time,
                                    "minutes_until": max(0, minutes_until),
                                    "due_time": self._format_due_time(minutes_until),
                                }
                            )

        # Sort by arrival time
        arrivals.sort(key=lambda x: x["arrival_timestamp"])

        return {
            "stop_id": stop_id,
            "arrivals": arrivals,
            "count": len(arrivals),
            "last_update": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def _format_due_time(minutes: int) -> str:
        """Format the due time in a human-readable way."""
        if minutes <= 0:
            return "Due"
        elif minutes == 1:
            return "1 min"
        elif minutes < 60:
            return f"{minutes} mins"
        else:
            hours = minutes // 60
            mins = minutes % 60
            if mins == 0:
                return f"{hours}h"
            return f"{hours}h {mins}m"
