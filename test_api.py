import requests

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
        "Host": "localhost"
    }
    response = requests.get(url, headers=headers)
    print(f"预约管理接口状态码: {response.status_code}")
    if response.status_code == 200:
        print("预约管理接口测试成功!")
        print("返回数据:", response.json())
    elif response.status_code == 404:
        print("预约管理接口测试失败: Site not found")
        print("响应文本:", response.text)
    else:
        print("预约管理接口测试失败!")
        try:
            print("错误信息:", response.json())
        except:
            print("响应文本:", response.text)

# 测试分类管理接口
def test_categories(token):
    url = "http://localhost:8001/api/v1/categories/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Host": "localhost"
    }
    response = requests.get(url, headers=headers)
    print(f"分类管理接口状态码: {response.status_code}")
    if response.status_code == 200:
        print("分类管理接口测试成功!")
        print("返回数据:", response.json())
    elif response.status_code == 404:
        print("分类管理接口测试失败: Site not found")
        print("响应文本:", response.text)
    else:
        print("分类管理接口测试失败!")
        try:
            print("错误信息:", response.json())
        except:
            print("响应文本:", response.text)

if __name__ == "__main__":
    token = get_token()
    if token:
        print(f"获取到token: {token[:20]}...")
        test_appointments(token)
        print("\n" + "-"*50 + "\n")
        test_categories(token)
