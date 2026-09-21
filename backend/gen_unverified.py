import os

with open('../docs/api-parity-matrix.md', 'r') as f:
    lines = f.readlines()

unverified = []
for line in lines:
    if 'IMPLEMENTED_NOT_VERIFIED' in line or 'REQUIRES REVIEW' in line:
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) >= 8:
            unverified.append({
                'id': parts[0],
                'method': parts[1],
                'endpoint': parts[2],
                'domain': parts[4],
                'auth': parts[5]
            })

content = "# Unverified Endpoints\n\n| # | Endpoint | Domain | Current Laravel Status | Missing Verification |\n| - | -------- | ------ | ---------------------- | -------------------- |\n"
for u in unverified:
    content += f"| {u['id']} | {u['method']} {u['endpoint']} | {u['domain']} | IMPLEMENTED_NOT_VERIFIED | Tests, Validation Parity, DB Side-effects |\n"

with open('../docs/unverified-endpoints.md', 'w') as f:
    f.write(content)

print(f"Found {len(unverified)} unverified endpoints.")
