"""Config flow for Dublin Bus RTPI integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .api import DublinBusAPI
from .const import CONF_ROUTE_FILTERS, CONF_STOP_IDS, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("api_key"): str,
        vol.Required(CONF_STOP_IDS): str,
        vol.Optional(CONF_ROUTE_FILTERS, default=""): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # Parse stop IDs
    stop_ids = [s.strip() for s in data[CONF_STOP_IDS].split(",") if s.strip()]
    if not stop_ids:
        raise InvalidStopIds

    # Parse route filters (optional)
    route_filters = []
    if data.get(CONF_ROUTE_FILTERS):
        route_filters = [
            r.strip() for r in data[CONF_ROUTE_FILTERS].split(",") if r.strip()
        ]

    # Test the API connection
    api = DublinBusAPI(
        api_key=data["api_key"],
        stop_ids=stop_ids,
        route_filters=route_filters,
    )

    try:
        await hass.async_add_executor_job(api.test_connection)
    except Exception as err:
        _LOGGER.error("Failed to connect to Dublin Bus API: %s", err)
        raise CannotConnect from err

    return {
        "title": f"Dublin Bus ({len(stop_ids)} stops)",
        "stop_ids": stop_ids,
        "route_filters": route_filters,
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dublin Bus RTPI."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidStopIds:
                errors["base"] = "invalid_stop_ids"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=info["title"],
                    data={
                        "api_key": user_input["api_key"],
                        "stop_ids": info["stop_ids"],
                        "route_filters": info["route_filters"],
                    },
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidStopIds(HomeAssistantError):
    """Error to indicate invalid stop IDs."""
