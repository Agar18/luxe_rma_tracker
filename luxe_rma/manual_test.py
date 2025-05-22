import requests

BASE = "http://localhost:5000"

# 1. Register
res = requests.post(f"{BASE}/auth/register", json={
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
})
print("Register:", res.status_code, res.json())

# 2. Login
res = requests.post(f"{BASE}/auth/login", json={
    "email": "test@example.com",
    "password": "password123"
})
print("Login:", res.status_code, res.json())

token = res.json().get("token")

headers = {"Authorization": f"Bearer {token}"}

# 3. Register Marker
res = requests.post(f"{BASE}/marker/register-marker", json={
    "serial_number": "LX000001",
    "model": "Luxe X",
    "color": "Blackout",
    "date_made": "2024-05-01",
    "user_id": 1,
    "purchased_from": "DealerX",
    "purchase_date": "2024-05-10"
}, headers=headers)
print("Register Marker:", res.status_code, res.json())
