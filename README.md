# Lietuvos savivaldybių aplinkosaugos reitingas

Interaktyvus savivaldybių aplinkosaugos reitingo žemėlapis, įterpiamas į am.lrv.lt puslapius.

| Metai | Įterpimo kodas |
|---|---|
| 2026 | `<script src="https://cdn.jsdelivr.net/gh/AplinkosMinisterija/aplinkos-saugos-reitingas@2026.1/2026/map-builder.js"></script>` |
| 2025 | `<script src="https://cdn.jsdelivr.net/gh/AplinkosMinisterija/aplinkos-saugos-reitingas@2026.1/2025/map-builder.js"></script>` |

Žemėlapis įterpiamas toje vietoje, kur yra `<script>` žymė.

## Nauji metai

1. Sukurti aplanką `<metai>/`, įdėti skaičiavimo Excel (į repo nekeliamas – `.gitignore`).
2. Nukopijuoti ir pritaikyti `2026/generate.py` (metai, spalvos), paleisti `python generate.py`.
3. Patikrinti `index.html` naršyklėje, commit, naujas tag (pvz. `2027.1`) ir atnaujinti nuorodą puslapyje.

Pataisymams sukurti naują tag (`2026.2`), o ne perrašyti esamą – jsDelivr talpina failus pagal tag.
