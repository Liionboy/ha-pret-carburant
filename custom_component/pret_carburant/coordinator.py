"""Data coordinator for Preț Carburant România integration."""

import logging
import re
from datetime import datetime, timedelta

import aiohttp
from bs4 import BeautifulSoup

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    BASE_URL,
    FUEL_TYPES,
    COUNTY_CITIES,
    DEFAULT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


async def async_create_coordinator(
    hass: HomeAssistant,
    county: str,
    scan_interval: int = DEFAULT_SCAN_INTERVAL,
) -> DataUpdateCoordinator:
    """Create and return a DataUpdateCoordinator."""
    city_slug = COUNTY_CITIES.get(county)
    if not city_slug:
        raise ValueError(f"Unknown county: {county}")

    url = f"{BASE_URL}/preturi-carburanti/{city_slug}"

    async def _async_update_data():
        """Fetch data from pretcarburant.ro."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"HTTP {resp.status} from {url}")
                    html = await resp.text()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

        return _parse_html(html, county, city_slug)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DOMAIN}_{county}",
        update_method=_async_update_data,
        update_interval=timedelta(minutes=scan_interval),
    )

    await coordinator.async_config_entry_first_refresh()
    return coordinator


def _parse_html(html: str, county: str, city_slug: str) -> dict:
    """Parse HTML from pretcarburant.ro and extract fuel price data."""
    soup = BeautifulSoup(html, "html.parser")
    result = {
        "county": county,
        "city_slug": city_slug,
        "updated_at": datetime.now().isoformat(),
        "fuel_prices": {},
        "cheapest_stations": [],
        "networks": [],
        "station_count": 0,
    }

    # --- Extract station count from title ---
    title = soup.title.string if soup.title else ""
    match = re.search(r"(\d+)\s+benzinării", title)
    if match:
        result["station_count"] = int(match.group(1))

    # --- Extract from JSON-LD Dataset ---
    for script in soup.find_all("script", type="application/ld+json"):
        if not script.string:
            continue
        try:
            import json
            data = json.loads(script.string)
        except (json.JSONDecodeError, TypeError):
            continue

        # Dataset with variableMeasured
        if isinstance(data, dict) and data.get("@type") == "Dataset":
            for var in data.get("variableMeasured", []):
                name = var.get("name", "")
                value = var.get("value")
                if value:
                    try:
                        price = float(value)
                    except (ValueError, TypeError):
                        continue
                    if "benzina 95" in name.lower() or "benzină 95" in name.lower():
                        result["fuel_prices"]["benzina_95"] = {"avg": price}
                    elif "motorina" in name.lower() and "premium" not in name.lower():
                        result["fuel_prices"]["motorina"] = {"avg": price}
                    elif "gpl" in name.lower():
                        result["fuel_prices"]["gpl"] = {"avg": price}
                    elif "benzina premium" in name.lower() or "benzină premium" in name.lower():
                        result["fuel_prices"]["benzina_premium"] = {"avg": price}
                    elif "motorina premium" in name.lower():
                        result["fuel_prices"]["motorina_premium"] = {"avg": price}

    # --- Extract cheapest prices from Table 0 ---
    tables = soup.find_all("table")
    if tables:
        cheapest_table = tables[0]
        rows = cheapest_table.find_all("tr")
        for row in rows[1:]:  # skip header
            cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            if len(cells) >= 4:
                fuel_name = cells[0].lower()
                price_text = cells[1]
                station_name = cells[2]
                station_address = cells[3]

                price_match = re.search(r"([\d.]+)", price_text)
                if price_match:
                    price = float(price_match.group(1))
                    fuel_key = None
                    if "benzina 95" in fuel_name or "benzină 95" in fuel_name:
                        fuel_key = "benzina_95"
                    elif "motorina" in fuel_name and "premium" not in fuel_name:
                        fuel_key = "motorina"
                    elif "gpl" in fuel_name:
                        fuel_key = "gpl"
                    elif "benzina premium" in fuel_name or "benzină premium" in fuel_name:
                        fuel_key = "benzina_premium"
                    elif "motorina premium" in fuel_name:
                        fuel_key = "motorina_premium"

                    if fuel_key:
                        if fuel_key not in result["fuel_prices"]:
                            result["fuel_prices"][fuel_key] = {}
                        result["fuel_prices"][fuel_key]["min"] = price
                        result["fuel_prices"][fuel_key]["station"] = station_name
                        result["fuel_prices"][fuel_key]["address"] = station_address

    # --- Extract network prices from Table 2 (if exists) ---
    if len(tables) >= 3:
        network_table = tables[2]
        for row in network_table.find_all("tr")[1:]:
            cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            if len(cells) >= 5:
                network = {
                    "name": cells[0],
                    "stations": cells[1],
                    "benzina_95": _parse_price(cells[2]),
                    "motorina": _parse_price(cells[3]),
                    "gpl": _parse_price(cells[4]),
                }
                result["networks"].append(network)

    # --- Extract top 10 cheapest stations from Table 1 ---
    if len(tables) >= 2:
        stations_table = tables[1]
        for row in stations_table.find_all("tr")[1:]:
            cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            if len(cells) >= 6:
                station = {
                    "rank": cells[0],
                    "name": cells[1],
                    "address": cells[2],
                    "benzina_95": _parse_price(cells[3]),
                    "motorina": _parse_price(cells[4]),
                    "gpl": _parse_price(cells[5]),
                }
                result["cheapest_stations"].append(station)

    return result


def _parse_price(text: str) -> float | None:
    """Parse a price string like '8.92' or '—'."""
    if not text or text in ("—", "-", "N/A", ""):
        return None
    try:
        return float(text.replace(",", "."))
    except (ValueError, TypeError):
        return None
