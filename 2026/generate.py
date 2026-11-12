"""Sugeneruoja 2026/map-builder.js ir output.json: paima 2025/map-builder.js
(2022-2025 duomenys) ir prideda 2026 m. duomenis iš Excel lapo "6-7. Reitingas"."""
import json, re, sys, shutil
from pathlib import Path
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).resolve().parent
SRC = HERE.parent / '2025' / 'map-builder.js'
XLSX = HERE / 'Duomenų skaičiavimas 2026 (shared).xlsx'
YEAR = '2026'
FIELDS = ['waste', 'energetics', 'construction', 'transport', 'climate',
          'comfort', 'water', 'biodiversity', 'awareness']

ws = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)['6-7. Reitingas']
rows = list(ws.iter_rows(min_row=4, values_only=True))
new = {}
for r in rows:
    if r[0] is None:
        continue
    for i, f in enumerate(FIELDS):
        place, name, score = r[i*4], r[i*4+1], r[i*4+2]
        if name:
            new.setdefault(name.strip(), {})[f] = {'place': int(place), 'score': round(score, 2)}
    place, name, score = r[36], r[37], r[39]   # vieta, savivaldybė, taškai iš 100
    if name:
        new.setdefault(name.strip(), {})['total'] = {'place': int(place), 'score': round(score, 2)}

js = SRC.read_text(encoding='utf-8')
m = re.search(r'^(    data: )(\{.*\})(,?)$', js, re.M)
data = json.loads(m.group(2))
mun_names = {x['name'] for x in json.loads(re.search(r'^    municipalities: (\{.*\}),?$', js, re.M).group(1))['municipalities']}

missing = set(data) - set(new) - {''}
extra = set(new) - set(data)
assert not missing and not extra, (missing, extra)
assert len(new) == 60 and all(len(v) == 10 for v in new.values()), 'trūksta kategorijų'
assert set(new) <= mun_names, set(new) - mun_names

for name, years in data.items():
    if name in new:
        years[YEAR] = {k: new[name][k] for k in FIELDS + ['total']}

out = js[:m.start(2)] + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + js[m.end(2):]
out = out.replace('aplinkosaugos reitingas 2025 m.', 'aplinkosaugos reitingas 2026 m.')
out = out.replace('currentYear: 2025,', 'currentYear: 2026,')
out = out.replace('APLINKOS SAUGOS REITINGAS 2025 m.', 'APLINKOS SAUGOS REITINGAS 2026 m.')
# 2026 m. spalvos – žalia (2024 mėlyna, 2025 violetinė)
for old, new_c in [("from: '#e8d5f2'", "from: '#d6ebdc'"), ("to: '#4a1a5c'", "to: '#1e4d2b'"),
                   ("winners: '#4a0963'", "winners: '#163a20'"), ('#9965a3', '#3f7d4f')]:
    assert old in out, old
    out = out.replace(old, new_c)
# Failo vardas nebesvarbus: script žymė nustatoma per document.currentScript
for old, new_c in [
    ("    places: `<g class=\"places\"></g>`,",
     "    scriptElement: document.currentScript,\n    places: `<g class=\"places\"></g>`,"),
    ("const mapBuilderScript = document.querySelector('script[src$=\"map-builder.js\"]');",
     "const mapBuilderScript = this.scriptElement || document.querySelector('script[src*=\"map-builder\"]');"),
    ('document.addEventListener("DOMContentLoaded", function () {\n    mapBuilder.init();\n});',
     'if (document.readyState === "loading") {\n    document.addEventListener("DOMContentLoaded", function () {\n        mapBuilder.init();\n    });\n} else {\n    mapBuilder.init();\n}'),
]:
    assert old in out, old
    out = out.replace(old, new_c)
assert '2025 m.' not in out
(HERE / 'map-builder.js').write_text(out, encoding='utf-8')
(HERE / 'output.json').write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding='utf-8')
shutil.copy(SRC.parent / 'index.html', HERE / 'index.html')

top = sorted(new.items(), key=lambda kv: -kv[1]['total']['score'])[:10]
for n, v in top:
    print(v['total']['place'], n, v['total']['score'])
