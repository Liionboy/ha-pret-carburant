"""Constants for Preț Carburant România integration."""

DOMAIN = "pret_carburant"
PLATFORM = "sensor"
CONF_COUNTY = "county"
CONF_CITY = "city"
CONF_FUEL_TYPES = "fuel_types"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 120  # minutes - matches source update frequency

BASE_URL = "https://pretcarburant.ro"

FUEL_TYPES = {
    "benzina_95": "Benzină Standard 95",
    "motorina": "Motorină Standard",
    "gpl": "GPL Auto",
    "benzina_premium": "Benzină Premium 98/100",
    "motorina_premium": "Motorină Premium",
}

FUEL_ICONS = {
    "benzina_95": "mdi:gas-station",
    "motorina": "mdi:gas-station",
    "gpl": "mdi:gas-station-outline",
    "benzina_premium": "mdi:gas-station",
    "motorina_premium": "mdi:gas-station",
}

# County slug -> display name mapping
# Based on pretcarburant.ro URL structure
COUNTIES = {
    "alba": "Alba",
    "arad": "Arad",
    "arges": "Argeș",
    "bacau": "Bacău",
    "bihor": "Bihor",
    "bistrita-nasaud": "Bistrița-Năsăud",
    "botosani": "Botoșani",
    "braila": "Brăila",
    "brasov": "Brașov",
    "bucuresti": "București",
    "buzau": "Buzău",
    "calarasi": "Călărași",
    "caras-severin": "Caraș-Severin",
    "cluj": "Cluj",
    "constanta": "Constanța",
    "covasna": "Covasna",
    "dambovita": "Dâmbovița",
    "dolj": "Dolj",
    "galati": "Galați",
    "giurgiu": "Giurgiu",
    "gorj": "Gorj",
    "harghita": "Harghita",
    "hunedoara": "Hunedoara",
    "ialomita": "Ialomița",
    "iasi": "Iași",
    "ilfov": "Ilfov",
    "maramures": "Maramureș",
    "mehedinti": "Mehedinți",
    "mures": "Mureș",
    "neamt": "Neamț",
    "olt": "Olt",
    "prahova": "Prahova",
    "salaj": "Sălaj",
    "satu-mare": "Satu Mare",
    "sibiu": "Sibiu",
    "suceava": "Suceava",
    "teleorman": "Teleorman",
    "timis": "Timiș",
    "tulcea": "Tulcea",
    "valcea": "Vâlcea",
    "vaslui": "Vaslui",
    "vrancea": "Vrancea",
}

# County slug -> primary city slug for URL
# pretcarburant.ro uses city slugs in URLs
COUNTY_CITIES = {
    "alba": "alba-iulia",
    "arad": "arad",
    "arges": "pitesti",
    "bacau": "bacau",
    "bihor": "oradea",
    "bistrita-nasaud": "bistrita",
    "botosani": "botosani",
    "braila": "braila",
    "brasov": "brasov",
    "bucuresti": "bucuresti",
    "buzau": "buzau",
    "calarasi": "calarasi",
    "caras-severin": "resita",
    "cluj": "cluj-napoca",
    "constanta": "constanta",
    "covasna": "sfantu-gheorghe",
    "dambovita": "targoviste",
    "dolj": "craiova",
    "galati": "galati",
    "giurgiu": "giurgiu",
    "gorj": "targu-jiu",
    "harghita": "miercurea-ciuc",
    "hunedoara": "deva",
    "ialomita": "slobozia",
    "iasi": "iasi",
    "ilfov": "voluntari",
    "maramures": "baia-mare",
    "mehedinti": "drobeta-turnu-severin",
    "mures": "targu-mures",
    "neamt": "piatra-neamt",
    "olt": "slatina",
    "prahova": "ploiesti",
    "salaj": "zalau",
    "satu-mare": "satu-mare",
    "sibiu": "sibiu",
    "suceava": "suceava",
    "teleorman": "alexandria",
    "timis": "timisoara",
    "tulcea": "tulcea",
    "valcea": "ramnicu-valcea",
    "vaslui": "vaslui",
    "vrancea": "focsani",
}
