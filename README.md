# HA Preț Carburant România

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Integrație Home Assistant pentru monitorizarea prețurilor la carburanți din România, pe județe.

![Romania Flag](https://img.shields.io/badge/🇷🇴-Romania-blue)

## 📊 Despre

Integrația preia date de la [PretCarburant.ro](https://pretcarburant.ro) — sursă oficială care monitorizează **1514 benzinării** din toată România, cu actualizare **la fiecare 2 ore**.

Datele provin din **Monitorul Prețurilor (ANPC / Consiliul Concurenței)** și feed-urile directe ale rețelelor (SOCAR, OSCAR, etc.).

## 🚀 Instalare

### HACS (recomandat)

1. Adaugă repository-ul ca **Custom Repository** în HACS:
   - HACS → Integrations → ⋮ → Custom repositories
   - URL: `https://github.com/Liionboy/ha-pret-carburant`
   - Category: Integration
2. Caută "Preț Carburant România" în HACS
3. Instalează
4. Restart Home Assistant

### Manual

1. Copiază directorul `custom_components/pret_carburant` în `config/custom_components/`
2. Restart Home Assistant

## ⚙️ Configurare

1. Settings → Devices & Services → + Add Integration
2. Caută "Preț Carburant România"
3. Selectează județul din dropdown
4. (Opțional) Setează intervalul de actualizare (default: 120 minute)

Repetați pentru fiecare județ pe care doriți să-l monitorizați.

## 📡 Senzori creați

Pentru fiecare județ configurat, se creează:

### Senzori de preț (per tip de carburant)

| Senzor | Descriere |
|--------|-----------|
| `sensor.pret_benzina_95_<judet>` | Preț minim Benzină Standard 95 |
| `sensor.pret_motorina_<judet>` | Preț minim Motorină Standard |
| `sensor.pret_gpl_<judet>` | Preț minim GPL Auto |
| `sensor.pret_benzina_premium_<judet>` | Preț minim Benzină Premium 98/100 |
| `sensor.pret_motorina_premium_<judet>` | Preț minim Motorină Premium |

### Senzor summary

| Senzor | Descriere |
|--------|-----------|
| `sensor.cea_mai_ieftina_statie_<judet>` | Cea mai ieftină stație din județ |

### Senzor rețele

| Senzor | Descriere |
|--------|-----------|
| `sensor.retele_carburanti_<judet>` | Comparație prețuri pe rețele (Petrom, OMV, Rompetrol, etc.) |

## 📋 Atribute suplimentare

Fiecare senzor de preț include:

```yaml
min_price: 8.92          # Prețul minim din județ
avg_price: 9.01          # Prețul mediu din județ
cheapest_station: Petrom  # Numele stației cu preț minim
cheapest_address: "str. Barbu Vacarescu, nr. 78"
county: București         # Numele județului
station_count: 147        # Numărul total de benzinării
updated_at: "2026-05-02T23:19:00"  # Ultima actualizare
```

## 🔔 Exemplu de automatizare

Alertă când benzina scade sub un prag:

```yaml
automation:
  - alias: "Alertă preț mic benzină"
    trigger:
      - platform: numeric_state
        entity_id: sensor.pret_benzina_95_bucuresti
        below: 9.00
    action:
      - service: notify.mobile_app
        data:
          title: "⛽ Benzină ieftină!"
          message: >
            Benzina 95 costă {{ states('sensor.pret_benzina_95_bucuresti') }} lei/L
            la {{ state_attr('sensor.pret_benzina_95_bucuresti', 'cheapest_station') }}
```

## 🗺️ Județe disponibile

Toate cele 42 de județe + București:

Alba, Arad, Argeș, Bacău, Bihor, Bistrița-Năsăud, Botoșani, Brăila, Brașov, **București**, Buzău, Călărași, Caraș-Severin, Cluj, Constanța, Covasna, Dâmbovița, Dolj, Galați, Giurgiu, Gorj, Harghita, Hunedoara, Ialomița, Iași, Ilfov, Maramureș, Mehedinți, Mureș, Neamț, Olt, Prahova, Sălaj, Satu Mare, Sibiu, Suceava, Teleorman, Timiș, Tulcea, Vâlcea, Vaslui, Vrancea

## 📝 Note

- Datele sunt actualizate la fiecare **2 ore** (ca sursa)
- Prețurile sunt cele **minime** din județ (nu medii)
- Sursa: [PretCarburant.ro](https://pretcarburant.ro) — date deschise, licență CC-BY 4.0
- Nu este necesară nicio cheie API

## 🤝 Contribuții

Contribuțiile sunt binevenite! Deschide un issue sau un PR pe [GitHub](https://github.com/Liionboy/ha-pret-carburant).

## 📄 Licență

MIT License — vezi [LICENSE](LICENSE)

## 🙏 Mulțumiri

- [PretCarburant.ro](https://pretcarburant.ro) pentru datele deschise
- [ANPC Monitorul Prețurilor](https://monitorulpreturilor.info) pentru sursa oficială
- Comunitatea Home Assistant România 🇷🇴
