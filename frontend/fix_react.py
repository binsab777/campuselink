import re
def fix(path):
    with open(path, 'r', encoding='utf-8') as f: c = f.read()
    # Let's just do an exact, safe replacement manually for the specific files
    c = c.replace('`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/auth/login",', '`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/auth/login`,')
    c = c.replace('`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/auth/register",', '`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/auth/register`,')
    c = c.replace('`${process.env.NEXT_PUBLIC_API_URL || \'http://localhost:8000\'}/api/v1/auth/me\',', '`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/auth/me`,')
    with open(path, 'w', encoding='utf-8') as f: f.write(c)

fix('src/app/login/page.tsx')
fix('src/app/register/page.tsx')
fix('src/context/AuthContext.tsx')
