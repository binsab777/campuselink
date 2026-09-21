import re

with open('src/app/login/page.tsx', 'r') as f:
    c = f.read()

c = re.sub(r'const res = await fetch\(\"http://localhost:8000/api/v1/auth/login\".*?login\(data\.access_token, data\.refresh_token\);', 
           r'''const { apiClient } = await import("@/services/apiClient");
      const data = await apiClient.post<any>("/auth/login", {
        username: email.trim(),
        password
      });
      login(data.access_token, data.refresh_token);''', c, flags=re.DOTALL)
c = c.replace('Cannot reach backend server on http://localhost:8000', 'Cannot reach backend server.')
with open('src/app/login/page.tsx', 'w') as f:
    f.write(c)

with open('src/app/register/page.tsx', 'r') as f:
    c = f.read()
c = re.sub(r'const res = await fetch\(\"http://localhost:8000/api/v1/auth/register\".*?setTimeout\(\(\) => \{', 
           r'''const { apiClient } = await import("@/services/apiClient");
      await apiClient.post("/auth/register", {
        email: email.trim(),
        password,
        role,
      });

      setSuccess(true);
      setTimeout(() => {''', c, flags=re.DOTALL)
with open('src/app/register/page.tsx', 'w') as f:
    f.write(c)

with open('src/context/AuthContext.tsx', 'r') as f:
    c = f.read()
c = re.sub(r'const res = await fetch\(\'http://localhost:8000/api/v1/auth/me\'.*?setUser\(data\);\s*\} else \{.*?setToken\(null\);\s*\}', 
           r'''const { apiClient } = await import("@/services/apiClient");
        const data = await apiClient.get<any>("/auth/me");
        setUser(data.data || data);
      } catch (err) {
        console.error('Failed to fetch user', err);
        localStorage.removeItem('access_token');
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        setToken(null);
      // Removed else block since exceptions handle failure''', c, flags=re.DOTALL)

with open('src/context/AuthContext.tsx', 'w') as f:
    f.write(c)
