import json, re, glob
def fully_clean(s):
    s = re.sub(r'\{[^}]*\}', '', s)
    s = re.sub(r'\$[a-zA-Z0-9_\->]+', '', s)
    s = re.sub(r'\d+', '', s)
    s = s.replace('//', '/').strip('/')
    return s

tested_urls_cleaned = set()
for file in glob.glob('../backend-laravel/tests/**/*.php', recursive=True):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        urls = re.findall(r"['\"](/api/v1/[^'\"]+)['\"]", content)
        urls2 = re.findall(r"['\"](/api/v1/[^'\"]+)['\"]\s*\.", content)
        for u in urls + urls2:
            tested_urls_cleaned.add(fully_clean(u))

print(tested_urls_cleaned)
