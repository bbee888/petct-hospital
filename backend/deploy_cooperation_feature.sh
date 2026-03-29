#!/bin/bash

# 医院合作统计功能部署脚本
# 用于快速部署数据库迁移和初始化

echo "======================================"
echo "医院合作统计功能部署"
echo "======================================"
echo ""

# 检查是否在 backend 目录
if [ ! -f "start.py" ]; then
    echo "错误：请在 backend 目录下运行此脚本"
    echo "用法：cd backend && ./deploy_cooperation_feature.sh"
    exit 1
fi

# 步骤 1：备份数据库
echo "步骤 1: 备份数据库..."
read -p "是否需要备份数据库？(y/n) " backup_choice
if [ "$backup_choice" = "y" ]; then
    read -p "请输入数据库名称 (默认：petct_manage_db): " db_name
    db_name=${db_name:-petct_manage_db}
    backup_file="${db_name}_backup_$(date +%Y%m%d_%H%M%S).sql"
    mysqldump -u root -p "$db_name" > "../$backup_file"
    echo "数据库已备份到：../$backup_file"
fi
echo ""

# 步骤 2：运行数据库迁移
echo "步骤 2: 运行数据库迁移，添加 is_cooperation 字段..."
python3 add_is_cooperation_field.py
if [ $? -ne 0 ]; then
    echo "错误：数据库迁移失败"
    exit 1
fi
echo "数据库迁移完成！"
echo ""

# 步骤 3：初始化现有数据
echo "步骤 3: 初始化现有医院数据..."
read -p "是否需要将所有现有医院标记为合作医院？(y/n) " init_choice
if [ "$init_choice" = "y" ]; then
    python3 init_hospital_cooperation.py
    if [ $? -ne 0 ]; then
        echo "错误：数据初始化失败"
        exit 1
    fi
    echo "数据初始化完成！"
else
    echo "跳过数据初始化步骤"
fi
echo ""

# 步骤 4：重启服务
echo "步骤 4: 重启后端服务..."
read -p "是否需要重启后端服务？(y/n) " restart_choice
if [ "$restart_choice" = "y" ]; then
    echo "正在重启服务..."
    # 这里可以根据实际情况添加重启命令
    echo "请手动重启服务：python3 start.py"
fi
echo ""

# 完成
echo "======================================"
echo "部署完成！"
echo "======================================"
echo ""
echo "下一步操作："
echo "1. 重启后端服务（如果尚未重启）"
echo "2. 访问前端页面查看'合作医院'统计"
echo "3. 测试医院合作状态的编辑功能"
echo ""
echo "详细说明请查看：COOPERATION_FEATURE_SUMMARY.md"
echo ""
