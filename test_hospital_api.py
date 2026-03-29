#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医院列表页 API 测试脚本
用于快速测试后端 API 是否正常工作
"""

import requests
import json
from typing import Dict, Any

# API 基础地址
API_BASE_URL = "http://localhost:8000/api"

def test_hospital_list_api():
    """测试医院列表 API"""
    print("=" * 60)
    print("🏥 医院列表 API 测试")
    print("=" * 60)
    
    # 测试参数
    test_cases = [
        {
            "name": "基础查询（第 1 页，10 条）",
            "params": {"page": 1, "size": 10},
            "expected_status": 200
        },
        {
            "name": "只显示合作医院",
            "params": {"page": 1, "size": 5, "is_cooperation": 1},
            "expected_status": 200
        },
        {
            "name": "搜索包含'协和'的医院",
            "params": {"page": 1, "size": 10, "title": "协和"},
            "expected_status": 200
        },
        {
            "name": "按等级筛选（三甲）",
            "params": {"page": 1, "size": 10, "level": "三甲"},
            "expected_status": 200
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[测试 {i}/{len(test_cases)}] {test_case['name']}")
        print("-" * 60)
        
        try:
            # 发送请求
            response = requests.get(
                f"{API_BASE_URL}/hospitals",
                params=test_case['params'],
                timeout=5
            )
            
            # 检查状态码
            if response.status_code != test_case['expected_status']:
                print(f"❌ 状态码错误：期望 {test_case['expected_status']}, 实际 {response.status_code}")
                failed += 1
                continue
            
            # 解析响应
            data = response.json()
            
            # 验证响应结构
            required_fields = ["items", "total", "page", "size"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"❌ 响应缺少字段：{missing_fields}")
                failed += 1
                continue
            
            # 显示结果
            print(f"✅ 状态码：{response.status_code}")
            print(f"📊 总数：{data['total']}")
            print(f"📄 页码：{data['page']}")
            print(f"📏 每页数量：{data['size']}")
            print(f"🏥 返回医院数：{len(data['items'])}")
            
            # 显示前 3 条医院数据
            if data['items']:
                print(f"\n📋 前 3 条医院数据:")
                for idx, hospital in enumerate(data['items'][:3], 1):
                    print(f"  {idx}. {hospital.get('name', 'Unknown')} - ¥{hospital.get('price', 0)}")
            
            passed += 1
            
        except requests.exceptions.ConnectionError:
            print("❌ 连接失败：无法连接到后端服务")
            print("💡 提示：请确保后端服务正在运行 (python3 start.py)")
            failed += 1
            break
        except requests.exceptions.Timeout:
            print("❌ 请求超时")
            failed += 1
        except Exception as e:
            print(f"❌ 测试失败：{str(e)}")
            failed += 1
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    print(f"✅ 通过：{passed}/{len(test_cases)}")
    print(f"❌ 失败：{failed}/{len(test_cases)}")
    
    if failed == 0:
        print("\n🎉 所有测试通过！后端 API 工作正常！")
        return True
    else:
        print("\n⚠️ 部分测试失败，请检查后端服务配置")
        return False

def test_cors():
    """测试 CORS 跨域配置"""
    print("\n" + "=" * 60)
    print("🔗 CORS 跨域测试")
    print("=" * 60)
    
    try:
        # 模拟前端请求（带 Origin 头）
        headers = {
            "Origin": "http://localhost:3001"
        }
        
        response = requests.get(
            f"{API_BASE_URL}/hospitals",
            params={"page": 1, "size": 1},
            headers=headers,
            timeout=5
        )
        
        # 检查 CORS 头
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Credentials": response.headers.get("Access-Control-Allow-Credentials")
        }
        
        print(f"📋 CORS 响应头:")
        for key, value in cors_headers.items():
            if value:
                print(f"  ✅ {key}: {value}")
            else:
                print(f"  ❌ {key}: 未设置")
        
        if cors_headers["Access-Control-Allow-Origin"]:
            print("\n✅ CORS 配置正确，前端可以正常访问")
            return True
        else:
            print("\n⚠️ CORS 未配置，前端可能会有跨域问题")
            print("💡 需要在后端添加 CORS 中间件")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败：{str(e)}")
        return False

def main():
    """主函数"""
    print("\n🚀 开始测试医院列表 API...\n")
    
    # 测试 API 功能
    api_ok = test_hospital_list_api()
    
    # 测试 CORS
    cors_ok = test_cors() if api_ok else False
    
    # 最终结论
    print("\n" + "=" * 60)
    print("🎯 最终结论")
    print("=" * 60)
    
    if api_ok and cors_ok:
        print("✅ 后端 API 完全就绪，可以开始前端联调！")
        print("\n下一步:")
        print("1. 启动前端：cd cnpetct && npm run dev")
        print("2. 访问：http://localhost:3001/hospitals")
        print("3. 打开浏览器控制台查看日志")
    elif api_ok and not cors_ok:
        print("⚠️ API 正常但 CORS 未配置")
        print("\n解决方案:")
        print("在 backend/app/main.py 中添加 CORS 中间件")
    else:
        print("❌ 后端服务未就绪")
        print("\n解决方案:")
        print("1. cd backend")
        print("2. python3 start.py")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
