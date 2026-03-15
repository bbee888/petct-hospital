import mysql.connector

# 连接数据库
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="petct_manage_db"
)

cursor = conn.cursor()

# 检查站点表数据
print("检查站点表数据:")
cursor.execute("SELECT * FROM sites")
sites = cursor.fetchall()
print(f"站点数量: {len(sites)}")
for site in sites:
    print(site)

# 检查用户表数据
print("\n检查用户表数据:")
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print(f"用户数量: {len(users)}")
for user in users:
    print(user)

# 检查医院表数据
print("\n检查医院表数据:")
cursor.execute("SELECT * FROM hospitals LIMIT 5")
hospitals = cursor.fetchall()
print(f"医院数量: {len(hospitals)}")
for hospital in hospitals:
    print(hospital)

# 检查预约表数据
print("\n检查预约表数据:")
cursor.execute("SELECT * FROM appointments LIMIT 5")
appointments = cursor.fetchall()
print(f"预约数量: {len(appointments)}")
for appointment in appointments:
    print(appointment)

# 检查分类表数据
print("\n检查分类表数据:")
cursor.execute("SELECT * FROM categories")
categories = cursor.fetchall()
print(f"分类数量: {len(categories)}")
for category in categories:
    print(category)

cursor.close()
conn.close()
