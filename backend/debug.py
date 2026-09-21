import json, re

with open('actual_fastapi_routes.json', encoding='utf-8') as f: fastapi = json.load(f)

def normalize_route(r):
    r = re.sub(r'\{([a-zA-Z0-9_]+)(:[^}]+)?\}', '{id}', r)
    return r.rstrip('/')

endpoints = {}
for r in fastapi:
    if not r['path'].startswith('/api/v1'): continue
    path = normalize_route(r['path'])
    method = r['method'].upper()
    endpoints[f"{method} {path}"] = path

print(endpoints['PUT /api/v1/students/me/skills/{id}'])

def normalize_test_url(u):
    u = re.sub(r'\{[^}]+\}', '{id}', u)
    u = re.sub(r'(?<=/)\d+(?=/|$)', '{id}', u)
    return u.rstrip('/')

print(normalize_test_url('/api/v1/students/me/skills/{$skillId}'))
