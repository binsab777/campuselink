import re

def rewrite_login():
    with open('src/app/login/page.tsx', 'r') as f:
        c = f.read()
    
    # We will replace the entire try-catch block for handleLogin
    old_try = """    try {
      const form = new URLSearchParams();
      form.append("username", email.trim());
      form.append("password", password);

      const res = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: form.toString(),
      });

      if (!res.ok) {
        let errorMsg = "Login failed";
        try {
          const data = await res.json();
          errorMsg = data.detail || errorMsg;
        } catch (_) {
          errorMsg = `Server error (${res.status})`;
        }
        setError(errorMsg);
        setLoading(false);
        return;
      }

      const data = await res.json();
      login(data.access_token, data.refresh_token);
    } catch (err: any) {
      setError(err?.message || "Network error: Cannot reach backend server on http://localhost:8000");
    }"""
    
    new_try = """    try {
      const { apiClient } = await import("@/services/apiClient");
      const data = await apiClient.post<any>("/auth/login", {
        username: email.trim(),
        password
      });
      login(data.access_token, data.refresh_token);
    } catch (err: any) {
      setError(err?.message || "Network error: Cannot reach backend server.");
    }"""
    
    c = c.replace(old_try, new_try)
    with open('src/app/login/page.tsx', 'w') as f:
        f.write(c)

rewrite_login()
