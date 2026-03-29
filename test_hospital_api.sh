#!/bin/bash
# 医院列表 API 手动测试脚本（使用 curl）

echo "============================================================"
echo "🏥 医院列表 API 测试"
echo "============================================================"
echo ""

API_BASE_URL="http://localhost:8000/api"

# 检查后端服务是否运行
echo "📡 检查后端服务..."
if ! curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL/hospitals?page=1&size=1" | grep -q "200\|401"; then
    echo "❌ 无法连接到后端服务"
    echo "💡 提示：请先启动后端服务 (cd backend && python3 start.py)"
    exit 1
fi

echo "✅ 后端服务正在运行"
echo ""

# 测试用例 1: 基础查询
echo "============================================================"
echo "[测试 1/4] 基础查询（第 1 页，10 条）"
echo "============================================================"
response=$(curl -s "$API_BASE_URL/hospitals?page=1&size=10")
echo "$response" | python3 -m json.tool | head -20
echo ""

# 测试用例 2: 合作医院
echo "============================================================"
echo "[测试 2/4] 只显示合作医院"
echo "============================================================"
response=$(curl -s "$API_BASE_URL/hospitals?page=1&size=5&is_cooperation=1")
echo "$response" | python3 -m json.tool | head -20
echo ""

# 测试用例 3: 搜索功能
echo "============================================================"
echo "[测试 3/4] 搜索包含'协和'的医院"
echo "============================================================"
response=$(curl -s "$API_BASE_URL/hospitals?page=1&size=10&title=协和")
echo "$response" | python3 -m json.tool | head -20
echo ""

# 测试用例 4: 等级筛选
echo "============================================================"
echo "[测试 4/4] 按等级筛选（三甲）"
echo "============================================================"
response=$(curl -s "$API_BASE_URL/hospitals?page=1&size=10&level=三甲")
echo "$response" | python3 -m json.tool | head -20
echo ""

echo "============================================================"
echo "🎯 测试完成！"
echo "============================================================"
echo ""
echo "下一步:"
echo "1. 如果看到 JSON 数据，说明 API 正常"
echo "2. 启动前端：cd cnpetct && npm run dev"
echo "3. 访问：http://localhost:3001/hospitals"
echo ""
