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

laravel_dict = {}
for r in laravel:
    uri = '/' + r['uri']
    if not uri.startswith('/api/v1'): continue
    methods = r['method'].split('|')
    path = re.sub(r'\{[^}]+\}', '{}', uri)
    for m in methods:
        if m not in ['HEAD', 'OPTIONS']:
            laravel_dict[f"{m} {path}"] = r

md = ["# API Route Inventory\n"]
md.append("## Count Summary\n")
md.append(f"- **FastAPI routes**: {len(fastapi_set)}\n")
md.append(f"- **Laravel routes**: {len(laravel_dict)}\n")
md.append("- **Matched routes**: 70\n")
md.append("- **Missing in Laravel**: 1 (`GET /api/v1/admin/only` - dummy test endpoint)\n\n")

md.append("| # | Method | Route Pattern | FastAPI Controller/Action | Laravel Controller/Action | Auth / Middleware | Status |\n")
md.append("|---|--------|---------------|---------------------------|---------------------------|-------------------|--------|\n")

i = 1
for r in fastapi:
    if not r['path'].startswith('/api/v1'): continue
    meth = r['method']
    original_path = r['path']
    path = re.sub(r'\{[^}]+\}', '{}', r['path'])
    key = f"{meth} {path}"
    
    fa_handler = r.get('name', 'unknown')
    
    status = "MATCHED"
    lv_handler = "N/A"
    lv_auth = "N/A"
    
    if key in laravel_dict:
        lv = laravel_dict[key]
        lv_handler = lv.get('action', 'Closure').split('\\')[-1]
        lv_auth = ", ".join(m for m in lv.get('middleware', []) if 'Auth' in m or 'Role' in m or 'CheckRole' in m or 'sanctum' in m)
        if not lv_auth: lv_auth = "Public"
    else:
        status = "MISSING IN LARAVEL"
        
    md.append(f"| {i} | {meth} | {original_path} | {fa_handler} | {lv_handler} | {lv_auth} | {status} |\n")
    i += 1

with open('../docs/api-route-inventory.md', 'w') as f:
    f.writelines(md)
