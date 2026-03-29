import requests
import json

# 登录获取token
def get_token():
    url = "http://localhost:8001/api/v1/auth/login"
    data = {"username": "admin", "password": "admin123"}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"登录失败: {response.status_code}")
        print(response.json())
        return None

# 测试预约管理接口
def test_appointments(token):
    url = "http://localhost:8001/api/v1/appointments/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Host": "localhost",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    print(f"预约管理接口状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"响应文本: {response.text}")
    if response.status_code == 200:
        print("预约管理接口测试成功!")
        print("返回数据:", response.json())
    else:
        print("预约管理接口测试失败!")

# 测试分类管理接口
def test_categories(token):
    url = "http://localhost:8001/api/v1/categories/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Host": "localhost",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    print(f"分类管理接口状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"响应文本: {response.text}")
    if response.status_code == 200:
        print("分类管理接口测试成功!")
        print("返回数据:", response.json())
    else:
        print("分类管理接口测试失败!")

# 测试其他接口，看看是否都有问题
def test_other_apis(token):
    apis = [
        "/api/v1/sites/",
        "/api/v1/hospitals/",
        "/api/v1/articles/",
        "/api/v1/tags/",
        "/api/v1/users/",
        "/api/v1/geo/tree/"
    ]
    
    for api in apis:
        url = f"http://localhost:8001{api}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Host": "localhost",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        print(f"\n测试接口: {api}")
        print(f"状态码: {response.status_code}")
        print(f"响应文本: {response.text[:200]}...")

if __name__ == "__main__":
    token = get_token()
    if token:
        print(f"获取到token: {token[:20]}...")
        print("\n" + "-"*50 + "\n")
        print("测试预约管理接口:")
        test_appointments(token)
        print("\n" + "-"*50 + "\n")
        print("测试分类管理接口:")
        test_categories(token)
        print("\n" + "-"*50 + "\n")
        print("测试其他接口:")
        test_other_apis(token)
