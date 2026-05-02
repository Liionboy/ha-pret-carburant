"""Sensor platform for Preț Carburant România integration."""

import logging
from datetime import datetime

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CONF_COUNTY,
    FUEL_TYPES,
    FUEL_ICONS,
    COUNTIES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    county = entry.data[CONF_COUNTY]
    county_name = COUNTIES.get(county, county)

    entities = []

    # One sensor per fuel type
    for fuel_key, fuel_name in FUEL_TYPES.items():
        entities.append(
            PretCarburantFuelSensor(
                coordinator, county, county_name, fuel_key, fuel_name
            )
        )

    # Summary sensor (cheapest station overall)
    entities.append(
        PretCarburantSummarySensor(coordinator, county, county_name)
    )

    # Network comparison sensor
    entities.append(
        PretCarburantNetworkSensor(coordinator, county, county_name)
    )

    async_add_entities(entities)


class PretCarburantFuelSensor(CoordinatorEntity, SensorEntity):
    """Sensor for a specific fuel type in a county."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "lei/L"
    _attr_device_class = SensorDeviceClass.MONETARY

    def __init__(self, coordinator, county, county_name, fuel_key, fuel_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._county = county
        self._county_name = county_name
        self._fuel_key = fuel_key

        self._attr_unique_id = f"pret_carburant_{county}_{fuel_key}"
        self._attr_name = f"{fuel_name} {county_name}"
        self._attr_icon = FUEL_ICONS.get(fuel_key, "mdi:gas-station")

    @property
    def native_value(self):
        """Return the minimum price for this fuel type."""
        data = self.coordinator.data
        if not data:
            return None
        fuel_data = data.get("fuel_prices", {}).get(self._fuel_key, {})
        return fuel_data.get("min") or fuel_data.get("avg")

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        data = self.coordinator.data
        if not data:
            return {}
        fuel_data = data.get("fuel_prices", {}).get(self._fuel_key, {})
        return {
            "min_price": fuel_data.get("min"),
            "avg_price": fuel_data.get("avg"),
            "cheapest_station": fuel_data.get("station"),
            "cheapest_address": fuel_data.get("address"),
            "county": self._county_name,
            "updated_at": data.get("updated_at"),
            "station_count": data.get("station_count"),
        }


class PretCarburantSummarySensor(CoordinatorEntity, SensorEntity):
    """Summary sensor showing cheapest station overall."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:gas-station"

    def __init__(self, coordinator, county, county_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._county = county
        self._county_name = county_name
        self._attr_unique_id = f"pret_carburant_{county}_summary"
        self._attr_name = f"Cea mai ieftină stație {county_name}"

    @property
    def native_value(self):
        """Return the cheapest station name."""
        data = self.coordinator.data
        if not data:
            return None
        stations = data.get("cheapest_stations", [])
        if stations:
            return stations[0].get("name")
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        data = self.coordinator.data
        if not data:
            return {}
        stations = data.get("cheapest_stations", [])
        if not stations:
            return {}
        cheapest = stations[0]
        return {
            "address": cheapest.get("address"),
            "benzina_95": cheapest.get("benzina_95"),
            "motorina": cheapest.get("motorina"),
            "gpl": cheapest.get("gpl"),
            "top_10": [
                {
                    "rank": s.get("rank"),
                    "name": s.get("name"),
                    "address": s.get("address"),
                    "benzina_95": s.get("benzina_95"),
                    "motorina": s.get("motorina"),
                    "gpl": s.get("gpl"),
                }
                for s in stations[:10]
            ],
            "county": self._county_name,
            "updated_at": data.get("updated_at"),
            "station_count": data.get("station_count"),
        }


class PretCarburantNetworkSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing price comparison across fuel networks."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:chart-bar"

    def __init__(self, coordinator, county, county_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._county = county
        self._county_name = county_name
        self._attr_unique_id = f"pret_carburant_{county}_networks"
        self._attr_name = f"Rețele carburanți {county_name}"

    @property
    def native_value(self):
        """Return number of networks."""
        data = self.coordinator.data
        if not data:
            return 0
        return len(data.get("networks", []))

    @property
    def extra_state_attributes(self):
        """Return network price comparison."""
        data = self.coordinator.data
        if not data:
            return {}
        networks = data.get("networks", [])
        return {
            "networks": [
                {
                    "name": n.get("name"),
                    "stations": n.get("stations"),
                    "benzina_95": n.get("benzina_95"),
                    "motorina": n.get("motorina"),
                    "gpl": n.get("gpl"),
                }
                for n in networks
            ],
            "county": self._county_name,
            "updated_at": data.get("updated_at"),
        }
