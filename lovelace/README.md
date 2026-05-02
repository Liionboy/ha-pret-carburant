# 🇷🇴 Preț Carburant România — Lovelace Cards

Acest director conține template-uri de carduri Lovelace pentru integrarea `pret_carburant`.

## Variante disponibile

### 1. `markdown_card.yaml` — Card Markdown (fără dependințe)
Funcționează cu orice instalare HA, fără carduri custom suplimentare.

### 2. `button_card.yaml` — Custom Button Card (necesită `custom:button-card`)
Carduri interactive cu styling avansat.

### 3. `full_dashboard.yaml` — Dashboard complet
Toate cardurile într-un layout organizat.

## Instalare

1. Copiază conținutul fișierului YAML dorit
2. În HA: Dashboard → Edit → Raw Configuration Editor
3. Lipește configurația
4. Înlocuiește `bucuresti` cu județul tău (ex: `cluj`, `timis`, `iasi`)
5. Salvează

## Senzori necesare

Asigură-te că ai integrarea `pret_carburant` configurată pentru județul dorit:
- `sensor.pret_benzina_95_<judet>`
- `sensor.pret_motorina_<judet>`
- `sensor.pret_gpl_<judet>`
- `sensor.pret_benzina_premium_<judet>`
- `sensor.pret_motorina_premium_<judet>`
- `sensor.cea_mai_ieftina_statie_<judet>`
- `sensor.retele_carburanti_<judet>`
