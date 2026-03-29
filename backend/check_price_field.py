#!/usr/bin/env python3
"""检查医院价格数据"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置环境变量
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./petct_manage.db'

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# 使用 SQLite 直接查询
db_path = os.path.join(os.path.dirname(__file__), 'petct_manage.db')
engine = create_engine(f'sqlite:///{db_path}')

with Session(engine) as session:
    # 查询所有列名
    from sqlalchemy import inspect
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('hospital')]
    print("hospital 表的列名:", columns)
    print()
    
    # 检查是否有 price 或 average_price 列
    if 'price' in columns:
        print("✓ 找到 'price' 列")
    elif 'average_price' in columns:
        print("✓ 找到 'average_price' 列")
    else:
        print("✗ 未找到价格列")
        print(f"可用列：{columns}")
    
    print("\n前 5 条记录:")
    result = session.execute(select("*").select_from("hospital")).fetchall()
    for row in result[:5]:
        print(row)
