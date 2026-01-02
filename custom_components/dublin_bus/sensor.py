"""Sensor platform for Dublin Bus RTPI integration."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import ATTRIBUTION, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Dublin Bus sensors from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]

    entities = []
    for stop_id in api.stop_ids:
        entities.append(DublinBusSensor(coordinator, stop_id))

    async_add_entities(entities)


class DublinBusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Dublin Bus stop sensor."""

    _attr_attribution = ATTRIBUTION
    _attr_icon = "mdi:bus"

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        stop_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._stop_id = stop_id
        self._attr_unique_id = f"dublin_bus_{stop_id}"
        self._attr_name = f"Dublin Bus Stop {stop_id}"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        if self.coordinator.data and self._stop_id in self.coordinator.data:
            return self.coordinator.data[self._stop_id]["count"]
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.coordinator.data or self._stop_id not in self.coordinator.data:
            return {}

        stop_data = self.coordinator.data[self._stop_id]
        
        # Format next buses for easy display
        next_buses = []
        for arrival in stop_data.get("arrivals", [])[:10]:  # Limit to next 10 buses
            next_buses.append(
                {
                    "route": arrival["route"],
                    "destination": arrival["destination"],
                    "due_time": arrival["due_time"],
                    "minutes_until": arrival["minutes_until"],
                }
            )

        return {
            "stop_id": self._stop_id,
            "stop_name": stop_data.get("stop_name"),
            "next_buses": next_buses,
            "last_update": stop_data.get("last_update"),
            "last_fetch_time": datetime.fromisoformat(stop_data.get("last_update")).strftime("%H:%M:%S"),
            "attribution": ATTRIBUTION,
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and self._stop_id in self.coordinator.data
        )
