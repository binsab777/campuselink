import requests

def test():
    # Login
    res = requests.post("http://localhost:8000/api/v1/auth/login", data={
        "username": "teststudent99@test.com",
        "password": "mypassword123"
    })
    token = res.json().get("access_token")
    if not token:
        print("Login failed:", res.json())
        return

    # Get profile
    res2 = requests.get("http://localhost:8000/api/v1/students/me", headers={
        "Authorization": f"Bearer {token}"
    })
    print("Profile response:", res2.json())

test()
