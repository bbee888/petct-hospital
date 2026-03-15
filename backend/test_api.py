import requests

BASE_URL = "http://localhost:8000"

# 测试根路径
print("Testing root endpoint...")
response = requests.get(f"{BASE_URL}/")
print(f"Root endpoint: {response.status_code} - {response.json()}")

# 测试登录
print("\nTesting login endpoint...")
login_data = {
    "username": "admin",
    "password": "admin123"
}
response = requests.post(
    f"{BASE_URL}/api/v1/auth/login",
    data=login_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
print(f"Login endpoint: {response.status_code}")
if response.status_code == 200:
    token_data = response.json()
    print(f"Token received: {token_data['access_token'][:20]}...")
    
    # 测试获取站点列表（需要认证）
    print("\nTesting sites endpoint (authenticated)...")
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    response = requests.get(f"{BASE_URL}/api/v1/sites/", headers=headers)
    print(f"Sites endpoint: {response.status_code}")
    if response.status_code == 200:
        sites = response.json()
        print(f"Sites count: {len(sites)}")
        for site in sites:
            print(f"  - {site['name']} ({site['domain']})")
else:
    print(f"Login failed: {response.text}")

print("\nAll tests completed!")