
import requests

BASE = "http://localhost:5000"

def print_result(label, res):
    print(f"\n[{label}]")
    print("Status Code:", res.status_code)
    try:
        print("Response:", res.json())
    except:
        print("Non-JSON Response:", res.text)

# 1. Auth & Security
res = requests.post(f"{BASE}/auth/register", json={
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
})
print_result("Auth - Register", res)

res = requests.post(f"{BASE}/auth/login", json={
    "email": "test@example.com",
    "password": "password123"
})
print_result("Auth - Login", res)

token = res.json().get("token")
user_id = res.json().get("user_id")
headers = {"Authorization": f"Bearer {token}"}

# 2. Marker Management
res = requests.post(f"{BASE}/marker/register-marker", json={
    "serial_number": "LX000001",
    "model": "Luxe X",
    "color": "Blackout",
    "date_made": "2024-05-01",
    "user_id": user_id,
    "purchased_from": "DealerX",
    "purchase_date": "2024-05-10"
}, headers=headers)
print_result("Marker - Register", res)

res = requests.get(f"{BASE}/marker/search/LX000001", headers=headers)
print_result("Marker - Search", res)

# 3. Ownership Tracking
print("\n[Ownership Tracking]")
print("Check ownership manually in pgAdmin for marker_id = 1 and user_id =", user_id)

# 4. RMA Flow
res = requests.post(f"{BASE}/rma/create", json={
    "marker_id": 1,
    "user_id": user_id
}, headers=headers)
print_result("RMA - Create", res)

# 5. Repair Logging
res = requests.post(f"{BASE}/repair/log", json={
    "marker_id": 1,
    "tech_id": user_id,
    "description": "Air leak test",
    "diagnosis": "Loose valve",
    "repair_date": "2024-05-21",
    "cost": 45.00,
    "warranty": False,
    "status": "in_progress"
}, headers=headers)
print_result("Repair - Log", res)

res = requests.get(f"{BASE}/repair/history/1", headers=headers)
print_result("Repair - History", res)

# 6. Email Notification
res = requests.post(f"{BASE}/notify/customer", json={
    "email": "test@example.com",
    "subject": "Test Email",
    "message": "This is a test RMA update from Luxe Paintball."
}, headers=headers)
print_result("Email - Notification", res)

# 7. Error Handling (Missing fields)
res = requests.post(f"{BASE}/auth/register", json={
    "email": "missing@field.com"
})
print_result("Error - Missing Registration Fields", res)

res = requests.post(f"{BASE}/marker/register-marker", json={
    "serial_number": "LX000002"
}, headers=headers)
print_result("Error - Incomplete Marker Registration", res)

# 8. Database Update Reminder
print("\n[Database Update]")
print("Verify all records are in pgAdmin (users, markers, ownerships, rmas, repairs).")
