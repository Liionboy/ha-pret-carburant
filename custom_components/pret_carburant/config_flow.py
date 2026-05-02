"""Config flow for Preț Carburant România integration."""

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_COUNTY,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    COUNTIES,
)

_LOGGER = logging.getLogger(__name__)


class PretCarburantConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Preț Carburant."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step - county selection."""
        errors = {}

        if user_input is not None:
            county = user_input[CONF_COUNTY]
            # Check for duplicate entries
            await self.async_set_unique_id(f"pret_carburant_{county}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Preț Carburant - {COUNTIES[county]}",
                data=user_input,
            )

        county_options = {k: v for k, v in sorted(COUNTIES.items(), key=lambda x: x[1])}

        schema = vol.Schema(
            {
                vol.Required(CONF_COUNTY): vol.In(county_options),
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(int, vol.Range(min=30, max=1440)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return PretCarburantOptionsFlow(config_entry)


class PretCarburantOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Preț Carburant."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.data.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=current_interval
                ): vol.All(int, vol.Range(min=30, max=1440)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
