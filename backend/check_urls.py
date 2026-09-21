import json, re, glob

with open('actual_fastapi_routes.json', encoding='utf-8') as f:
    fastapi = json.load(f)

tested_urls = set()
for file in glob.glob('../backend-laravel/tests/**/*.php', recursive=True):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        urls = re.findall(r"['\"](/api/v1/[^'\"]+)['\"]", content)
        for u in urls:
            u_clean = re.sub(r'\{[^}]+\}', '{}', u)
            u_clean = re.sub(r'\$[a-zA-Z0-9_\->]+', '{}', u_clean)
            u_clean = re.sub(r'\d+', '{}', u_clean)
            tested_urls.add(u_clean.strip('/'))

print("TESTED_URLS:", tested_urls)
