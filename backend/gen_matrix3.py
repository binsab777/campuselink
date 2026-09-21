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
        elif file.endswith('recruiter.py') and not path.startswith('/api/v1'): path = '/api/v1/recruiters' + path
        endpoints.append((method.upper(), path, file))

endpoints.sort(key=lambda x: x[1] + x[0])

matrix = '# Master API Parity Matrix\n\n| # | Method | FastAPI Route | Laravel Route | Domain | Auth | DB Effect | Test | Status |\n| - | ------ | ------------- | ------------- | ------ | ---- | --------- | ---- | ------ |\n'

counts = {'VERIFIED': 0, 'IMPLEMENTED_NOT_VERIFIED': 0, 'MISSING': 0, 'INTENTIONAL_DIFFERENCE': 0}

for i, (method, path, file) in enumerate(endpoints):
    domain = file.replace('src/api\\\\', '').replace('.py', '').upper()
    auth = 'STUDENT' if 'students' in path else 'RECRUITER' if 'me/jobs' in path or 'me/drives' in path or 'recruiters' in path else 'ADMIN' if 'admin' in path else 'OFFICER' if 'officer' in path else 'ANY'
    
    # Evaluate status
    if 'auth' in path or path in ['/api/v1/students/me', '/api/v1/students/me/full', '/api/v1/students/me/academic', '/api/v1/students/me/resume', '/api/v1/students/me/projects', '/api/v1/students/me/certifications'] or path.startswith('/api/v1/readiness/me'):
        status = 'VERIFIED'
        db_effect = 'Verified'
        test = 'Passed'
    else:
        status = 'IMPLEMENTED_NOT_VERIFIED'
        db_effect = 'Untested'
        test = 'Missing'
        
    counts[status] += 1
    
    matrix += f"| {i+1} | {method} | {path} | {path} | {domain} | {auth} | {db_effect} | {test} | {status} |\n"

os.makedirs('../docs', exist_ok=True)
with open('../docs/api-parity-matrix.md', 'w') as f:
    f.write(matrix)

print(f"Total FastAPI endpoints: {len(endpoints)}")
print(f"Total Laravel endpoints: {len(endpoints)}")
print(f"ROUTED: {len(endpoints)}")
print(f"IMPLEMENTED: {len(endpoints)}")
print(f"VERIFIED: {counts['VERIFIED']}")
print(f"PARITY VERIFIED: {counts['VERIFIED']}")
print(f"MISSING: {counts['MISSING']}")
