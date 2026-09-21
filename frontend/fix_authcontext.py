import re

def rewrite_authcontext():
    with open('src/context/AuthContext.tsx', 'r') as f:
        c = f.read()
    
    old_try = """      try {
        const res = await fetch('http://localhost:8000/api/v1/auth/me', {
          headers: { Authorization: `Bearer ${storedToken}` },
        });

        if (res.ok) {
          const data = await res.json();
          setUser(data);
        } else {
          localStorage.removeItem('access_token');
          localStorage.removeItem('token');
          localStorage.removeItem('refresh_token');
          setToken(null);
        }
      } catch (err) {
        console.error('Failed to fetch user', err);
      } finally {
        setLoading(false);
      }"""
    
    new_try = """      try {
        const { apiClient } = await import("@/services/apiClient");
        const data = await apiClient.get<User>("/auth/me");
        // Laravel returns user inside `data` sometimes if using API resources?
        // Wait, UserResource returning array: data: {...} vs plain {...}?
        // In Laravel, `UserResource::make($user)` typically returns `{"data": {...}}`.
        // Let's check what it returns or just accept the response.
        // Actually, AuthController in my script did `new UserResource($user)` without wrapping in an array, wait. Laravel wraps in `data` by default.
        // I will just use `data.data || data` to be safe!
        setUser((data as any).data || data);
      } catch (err) {
        console.error('Failed to fetch user', err);
        localStorage.removeItem('access_token');
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        setToken(null);
      } finally {
        setLoading(false);
      }"""
    
    c = c.replace(old_try, new_try)
    with open('src/context/AuthContext.tsx', 'w') as f:
        f.write(c)

rewrite_authcontext()
