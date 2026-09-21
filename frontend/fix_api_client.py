import re
with open('src/services/apiClient.ts', 'r') as f:
    c = f.read()

laravel_handler = """
    // Laravel 422 format
    if (error.errors && typeof error.errors === "object" && !Array.isArray(error.errors)) {
      Object.keys(error.errors).forEach((key) => {
        const val = error.errors[key];
        fieldErrors[key] = Array.isArray(val) ? val[0] : val;
      });
      return { message: error.message || "Validation error", fieldErrors, status };
    }
"""

if '// Laravel 422 format' not in c:
    c = c.replace('if (Array.isArray(error.detail)) {', laravel_handler + '\n    if (Array.isArray(error.detail)) {')
    with open('src/services/apiClient.ts', 'w') as f: f.write(c)
