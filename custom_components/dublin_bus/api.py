"""API client for Dublin Bus RTPI using TFI LTS API."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
import json
from typing import Any

import requests

from .const import API_LOOKUP, API_DEPARTURES

_LOGGER = logging.getLogger(__name__)

# The working subscription key used by the TFI website for public departures
TFI_LTS_KEY = "630688984d38409689932a37a8641bb9"

class DublinBusAPI:
    """API client for Dublin Bus real-time information."""

    def __init__(
        self,
        api_keys: list[str],
        stop_ids: list[str],
        route_filters: list[str] | None = None,
    ) -> None:
        """Initialize the API client."""
        # We store these keys but use the known working TFI key for the LTS API
        self.api_keys = api_keys
        self.stop_ids = stop_ids
        self.route_filters = route_filters or []
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": TFI_LTS_KEY,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://journeyplanner-production.transportforireland.ie",
            "Referer": "https://journeyplanner-production.transportforireland.ie/"
        })
        self._stop_metadata = {}

    def _get_full_stop_info(self, stop_id: str) -> dict[str, Any] | None:
        """Lookup stop name and full ID from short code."""
        if stop_id in self._stop_metadata:
            return self._stop_metadata[stop_id]

        payload = {
            "query": str(stop_id),
            "excludeStopArea": False,
            "language": "en"
        }
        
        try:
            response = self.session.post(API_LOOKUP, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Exact match search
            for item in data:
                if str(item.get("shortCode")) == str(stop_id) or str(item.get("id")).endswith(str(stop_id)):
                    self._stop_metadata[stop_id] = {
                        "full_id": item["id"],
                        "name": item["name"],
                        "type": item["type"]
                    }
                    return self._stop_metadata[stop_id]
            
            # Substring match for BUS_STOPS
            for item in data:
                if item.get("type") == "BUS_STOP" and str(stop_id) in str(item.get("shortCode", "")):
                    self._stop_metadata[stop_id] = {
                        "full_id": item["id"],
                        "name": item["name"],
                        "type": item["type"]
                    }
                    return self._stop_metadata[stop_id]

        except Exception as err:
            _LOGGER.error("Error looking up stop %s: %s", stop_id, err)
        
        return None

    def test_connection(self) -> bool:
        """Test by looking up the first stop."""
        if not self.stop_ids:
            return False
        return self._get_full_stop_info(self.stop_ids[0]) is not None

    def get_stop_data(self) -> dict[str, Any]:
        """Fetch real-time data for configured stops."""
        stops_data = {}
        now_ts = datetime.now(timezone.utc)
        now_str = now_ts.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        for stop_id in self.stop_ids:
            meta = self._get_full_stop_info(stop_id)
            if not meta:
                continue

            payload = {
                "clientTimeZoneOffsetInMS": 0,
                "departureDate": now_str,
                "departureOrArrival": "DEPARTURE",
                "departureTime": now_str,
                "refresh": False,
                "requestTime": now_str,
                "stopIds": [meta["full_id"]],
                "stopName": meta["name"],
                "stopType": meta["type"]
            }

            try:
                # Extra safety: ensure the session still has the correct key
                self.session.headers["Ocp-Apim-Subscription-Key"] = TFI_LTS_KEY
                
                response = self.session.post(API_DEPARTURES, json=payload, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                arrivals = []
                for dep in data.get("stopDepartures", []):
                    route = dep.get("serviceNumber")
                    
                    if self.route_filters and route not in self.route_filters:
                        continue

                    # Parse time
                    time_str = dep.get("realTimeDeparture") or dep.get("scheduledDeparture")
                    if not time_str:
                        continue
                        
                    try:
                        # Normalize timezone
                        time_str_norm = time_str.replace("Z", "+00:00")
                        dt = datetime.fromisoformat(time_str_norm)
                        diff = int((dt - now_ts).total_seconds() / 60)
                        
                        if diff >= -1:
                            arrivals.append({
                                "route": route,
                                "destination": dep.get("destination", "Unknown"),
                                "arrival_timestamp": dt.timestamp(),
                                "minutes_until": max(0, diff),
                                "due_time": self._format_due_time(diff),
                            })
                    except Exception as e:
                        _LOGGER.debug("Error parsing time %s: %s", time_str, e)

                arrivals.sort(key=lambda x: x["arrival_timestamp"])

                stops_data[stop_id] = {
                    "stop_id": stop_id,
                    "stop_name": meta["name"],
                    "arrivals": arrivals,
                    "count": len(arrivals),
                    "last_update": now_ts.isoformat(),
                }

            except Exception as err:
                _LOGGER.error("Error fetching departures for %s: %s", stop_id, err)

        return stops_data

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
