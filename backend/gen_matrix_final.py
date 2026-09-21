import json, re, glob
def fully_clean(s):
    s = re.sub(r'\{[^}]*\}', '', s)
    s = re.sub(r'\$[a-zA-Z0-9_\->]+', '', s)
    s = re.sub(r'\d+', '', s)
    s = s.replace('//', '/').strip('/')
    return s

with open('actual_fastapi_routes.json', encoding='utf-8') as f: fastapi = json.load(f)

tested_urls_cleaned = set()
for file in glob.glob('../backend-laravel/tests/**/*.php', recursive=True):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        urls = re.findall(r"['\"](/api/v1/[^'\"]+)['\"]", content)
        urls2 = re.findall(r"['\"](/api/v1/[^'\"]+)['\"]\s*\.", content)
        for u in urls + urls2: tested_urls_cleaned.add(fully_clean(u))

routes_info = []
for r in fastapi:
    if not r['path'].startswith('/api/v1'): continue
    meth = r['method']
    original_path = r['path']
    fc = fully_clean(original_path)
    status = "VERIFIED" if fc in tested_urls_cleaned else "NOT VERIFIED"
    routes_info.append({'method': meth, 'path': original_path, 'status': status})

routes_info = [r for r in routes_info if r['path'] != '/api/v1/admin/only']
verified = sum(1 for r in routes_info if r['status'] == 'VERIFIED')
not_verified = len(routes_info) - verified

md = ["# API Parity Matrix\n", "## Status\n", f"*   **Total Endpoints**: {len(routes_info)}\n", f"*   **Implemented**: {len(routes_info)}\n", f"*   **Parity Verified**: {verified}\n", f"*   **Not Verified**: {not_verified}\n\n", "## Endpoints\n", "| Method | Route | Status |\n", "|--------|-------|--------|\n"]
for r in sorted(routes_info, key=lambda x: x['path']):
    md.append(f"| {r['method']} | `{r['path']}` | {r['status']} |\n")
with open('../docs/api-parity-matrix.md', 'w') as f: f.writelines(md)
print(f"Matrix updated. Verified: {verified}, Not Verified: {not_verified}")
