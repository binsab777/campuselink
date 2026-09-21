import re
content = open('../backend-laravel/tests/Feature/ApiParity/StudentProfileExtensionsParityTest.php').read()
matches = re.finditer(r'public\s+function\s+(test_[A-Za-z0-9_]+)', content)
test_methods = [(m.start(), m.group(1)) for m in matches]
calls = re.finditer(r'->(get|post|put|patch|delete)(?:Json)?\s*\(\s*[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
for call in calls:
    if 'students/me' in call.group(2):
        print(call.group(1), call.group(2))
