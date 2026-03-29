import mysql.connector

# 连接数据库
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
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

# 检查appointments表数据
print("\n检查appointments表数据:")
cursor.execute("SELECT * FROM appointments LIMIT 5")
appointments = cursor.fetchall()
print(f"预约数量: {len(appointments)}")
for appointment in appointments:
    print(appointment)

# 检查categories表数据
print("\n检查categories表数据:")
cursor.execute("SELECT * FROM categories")
categories = cursor.fetchall()
print(f"分类数量: {len(categories)}")
for category in categories:
    print(category)

# 检查hospitals表数据
print("\n检查hospitals表数据:")
cursor.execute("SELECT * FROM hospitals LIMIT 5")
hospitals = cursor.fetchall()
print(f"医院数量: {len(hospitals)}")
for hospital in hospitals:
    print(hospital)

# 检查articles表数据
print("\n检查articles表数据:")
cursor.execute("SELECT * FROM articles LIMIT 5")
articles = cursor.fetchall()
print(f"文章数量: {len(articles)}")
for article in articles:
    print(article)

cursor.close()
conn.close()
