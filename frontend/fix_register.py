import re

def rewrite_register():
    with open('src/app/register/page.tsx', 'r') as f:
        c = f.read()
    
    old_try = """    try {
      const res = await fetch("http://localhost:8000/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email.trim(),
          password,
          role,
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({ detail: "Registration failed." }));
        const parsed = parseApiError(data);
        setFormError(parsed.message);
        setFieldErrors(parsed.fieldErrors);
        setLoading(false);
        return;
      }

      setSuccess(true);
      setTimeout(() => {
        router.push("/login");
      }, 2000);
    } catch (err: any) {
      setFormError(err?.message || "Network error. Please try again.");
    }"""
    
    new_try = """    try {
      const { apiClient } = await import("@/services/apiClient");
      await apiClient.post("/auth/register", {
        email: email.trim(),
        password,
        role,
      });

      setSuccess(true);
      setTimeout(() => {
        router.push("/login");
      }, 2000);
    } catch (err: any) {
      setFormError(err?.message || "Registration failed.");
      if (err.fieldErrors) {
        setFieldErrors(err.fieldErrors);
      }
    }"""
    
    c = c.replace(old_try, new_try)
    with open('src/app/register/page.tsx', 'w') as f:
        f.write(c)

rewrite_register()
