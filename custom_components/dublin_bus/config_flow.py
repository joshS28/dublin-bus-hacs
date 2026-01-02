"""Config flow for Dublin Bus RTPI integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

from .api import DublinBusAPI
from .const import CONF_ROUTE_FILTERS, CONF_STOP_IDS, CONF_SCAN_INTERVAL, DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("primary_api_key"): str,
        vol.Optional("secondary_api_key"): str,
        vol.Required("stop_ids"): str,
        vol.Optional("route_filters"): str,
        vol.Optional("scan_interval", default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=10, max=300)
        ),
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    api_keys = [data["primary_api_key"]]
    if data.get("secondary_api_key"):
        api_keys.append(data["secondary_api_key"])

    stop_ids = [s.strip() for s in data["stop_ids"].split(",")]
    if not stop_ids:
        raise InvalidStopIds

    route_filters = []
    if data.get("route_filters"):
        route_filters = [r.strip() for r in data["route_filters"].split(",")]

    api = DublinBusAPI(api_keys, stop_ids, route_filters)
    
    # Run the test in a separate thread because it's blocking
    result = await hass.async_add_executor_job(api.test_connection)
    
    if not result:
        raise CannotConnect

    return {
        "title": f"Dublin Bus ({len(stop_ids)} stops)",
        "stop_ids": stop_ids,
        "route_filters": route_filters,
    }

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dublin Bus RTPI."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler()

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
            except Exception: # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=info["title"],
                    data={
                        "primary_api_key": user_input["primary_api_key"],
                        "secondary_api_key": user_input.get("secondary_api_key"),
                        "stop_ids": info["stop_ids"],
                        "route_filters": info["route_filters"],
                    },
                    options={
                        CONF_SCAN_INTERVAL: user_input.get("scan_interval", DEFAULT_SCAN_INTERVAL)
                    }
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for Dublin Bus."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
                }
            ),
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidStopIds(HomeAssistantError):
    """Error to indicate stop IDs are invalid."""
