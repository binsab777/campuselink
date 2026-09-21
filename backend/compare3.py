import json, re

with open('actual_fastapi_routes.json', encoding='utf-8') as f:
    fastapi = json.load(f)

fastapi_set = set()
for r in fastapi:
    if r['path'].startswith('/api/v1'):
        path = re.sub(r'\{[^}]+\}', '{}', r['path'])
        fastapi_set.add(f"{r['method']} {path}")

with open('../backend-laravel/laravel_routes_raw.json', encoding='utf-16') as f:
    laravel = json.load(f)

laravel_set = set()
for r in laravel:
    uri = '/' + r['uri']
    if not uri.startswith('/api/v1'): continue
    methods = r['method'].split('|')
    path = re.sub(r'\{[^}]+\}', '{}', uri)
    for m in methods:
        if m not in ['HEAD', 'OPTIONS']:
            laravel_set.add(f"{m} {path}")

print('FastAPI only:', len(fastapi_set - laravel_set))
for x in sorted(fastapi_set - laravel_set): print(' ', x)

print('\nLaravel only:', len(laravel_set - fastapi_set))
for x in sorted(laravel_set - fastapi_set): print(' ', x)

print(f'\nFastAPI count: {len(fastapi_set)}, Laravel count: {len(laravel_set)}')
