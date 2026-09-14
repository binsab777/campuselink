import requests

base_url = "http://localhost:8000/api/v1"

print("--- Registering proper recruiter ---")
reg_data = {
    "email": "testrecruiter_real@test.com",
    "password": "mypassword123",
    "role": "RECRUITER"
}
r = requests.post(f"{base_url}/auth/register", json=reg_data)
if r.status_code in [200, 201]:
    print("Recruiter registered successfully.")
elif r.status_code == 400 and "already registered" in r.text:
    print("Already registered!")
else:
    print("Error:", r.status_code, r.text)
