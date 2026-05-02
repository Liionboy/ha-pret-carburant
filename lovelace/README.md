# 🇷🇴 Preț Carburant România — Lovelace Cards

Acest director conține template-uri de carduri Lovelace pentru integrarea `pret_carburant`.

## Variante disponibile

### 1. `arges_card.yaml` — Card pentru județul Argeș ✅ Recomandat
Card complet cu Mushroom Template, fără dependințe suplimentare (doar `card-mod`).

### 2. `markdown_card.yaml` — Card pentru București (cu Mushroom)
Similar cu arges_card, dar pentru București. Necesită `custom:mushroom-card` + `card-mod`.

### 3. `simple_card.yaml` — Card simplu (fără dependințe)
Funcționează cu orice instalare HA standard, fără carduri custom suplimentare.

### 4. `full_dashboard.yaml` — Dashboard complet
Toate cardurile într-un layout organizat cu gauge-uri.

## Ce include fiecare card

- 💰 Prețuri minime pe tip de carburant (Benzină 95, Motorină, GPL, Premium)
- 🏆 Cea mai ieftină stație + adresă
- 🏅 Top 5/10 cele mai ieftine stații
- 📊 Comparație prețuri pe rețele (Petrom, OMV, Rompetrol, MOL, Lukoil, SOCAR)
- 💵 Calculator cost plin 50L
- 💡 Economie cu GPL față de benzină
- 🇷🇴 Header cu culorile României

## Instalare

1. Copiază conținutul fișierului YAML dorit
2. În HA: Dashboard → Edit → Raw Configuration Editor
3. Lipește configurația
4. **Înlocuiește numele județului** din entity IDs (ex: `bucuresti` → `arges`, `cluj`, `timis`)
5. Salvează

## Dependințe opționale

- **Mushroom Cards** (`custom:mushroom-card`) — pentru carduri cu design modern
- **card-mod** — pentru styling CSS custom (gradient header, border colors)
- **browser_mod** — pentru popup-uri interactive (opțional)

Fără acestea, folosește `simple_card.yaml` care funcționează cu HA standard.

## Senzori necesare

Asigură-te că ai integrarea `pret_carburant` configurată:
- `sensor.benzina_standard_95_<judet>`
- `sensor.motorina_standard_<judet>`
- `sensor.gpl_auto_<judet>`
- `sensor.benzina_premium_98_100_<judet>`
- `sensor.motorina_premium_<judet>`
- `sensor.cea_mai_ieftina_statie_<judet>`
- `sensor.retele_carburanti_<judet>`
