import glob, re, os

endpoints = []
for file in glob.glob('src/api/*.py'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'@router\.(get|post|put|patch|delete)\("([^"]+)"', content)
    for method, path in matches:
        if file.endswith('auth.py') and not path.startswith('/api/v1'): path = '/api/v1/auth' + path
        elif file.endswith('student.py') and not path.startswith('/api/v1'): path = '/api/v1/students' + path
        elif file.endswith('readiness.py') and not path.startswith('/api/v1'): path = '/api/v1/readiness' + path
        endpoints.append((method.upper(), path, file))

endpoints.sort(key=lambda x: x[1] + x[0])

matrix = '# API Parity Matrix\n\n| # | HTTP | FastAPI Endpoint | Laravel Endpoint | Domain | Auth | Status |\n| - | ---- | ---------------- | ---------------- | ------ | ---- | ------ |\n'

for i, (method, path, file) in enumerate(endpoints):
    domain = file.replace('src/api\\\\', '').replace('.py', '').upper()
    auth = 'STUDENT' if 'students' in path else 'RECRUITER' if 'me/jobs' in path or 'me/drives' in path else 'ADMIN' if 'admin' in path else 'OFFICER' if 'officer' in path else 'ANY'
    
    status = 'REQUIRES REVIEW'
    
    matrix += f"| {i+1} | {method} | {path} | {path} | {domain} | {auth} | {status} |\n"

os.makedirs('../docs', exist_ok=True)
with open('../docs/api-parity-matrix.md', 'w') as f:
    f.write(matrix)
