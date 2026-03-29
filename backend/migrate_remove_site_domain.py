#!/usr/bin/env python3
"""
数据库迁移脚本：删除 articles 表的 site_domain 字段

由于 articles 表通过 category_id 关联到 article_categories 表，
而 article_categories 表已经有 site_domain 字段，因此 articles 表的 site_domain 字段是多余的。
"""

import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'petct.db')

    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return

    # 备份数据库
    backup_path = db_path + '.backup'
    import shutil
    shutil.copy2(db_path, backup_path)
    print(f"数据库已备份到: {backup_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 检查 articles 表是否有 site_domain 字段
        cursor.execute("PRAGMA table_info(articles)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'site_domain' not in columns:
            print("articles 表没有 site_domain 字段，无需迁移")
            return

        print("开始迁移...")

        # 步骤 1: 创建新的 articles 表(不包含 site_domain)
        cursor.execute("""
            CREATE TABLE articles_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                title VARCHAR(100) NOT NULL,
                seo_keywords VARCHAR(120),
                seo_description VARCHAR(255),
                content TEXT NOT NULL,
                cover VARCHAR(100),
                view_count INTEGER DEFAULT 0,
                is_published BOOLEAN DEFAULT 0,
                published_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES article_categories(id) ON DELETE CASCADE
            )
        """)

        # 步骤 2: 将数据从旧表复制到新表
        cursor.execute("""
            INSERT INTO articles_new (
                id, category_id, title, seo_keywords, seo_description,
                content, cover, view_count, is_published, published_at
            )
            SELECT
                id, category_id, title, seo_keywords, seo_description,
                content, cover, view_count, is_published, published_at
            FROM articles
        """)

        copied_rows = cursor.rowcount
        print(f"已复制 {copied_rows} 条记录")

        # 步骤 3: 删除旧表
        cursor.execute("DROP TABLE articles")

        # 步骤 4: 重命名新表
        cursor.execute("ALTER TABLE articles_new RENAME TO articles")

        # 步骤 5: 重建索引
        cursor.execute("CREATE INDEX ix_articles_id ON articles (id)")
        cursor.execute("CREATE INDEX ix_articles_category_id ON articles (category_id)")

        # 提交事务
        conn.commit()

        print("迁移完成!")
        print(f"- 已删除 articles 表的 site_domain 字段")
        print(f"- 迁移了 {copied_rows} 条记录")
        print(f"- 数据库备份保存在: {backup_path}")

    except Exception as e:
        conn.rollback()
        print(f"迁移失败: {e}")
        print("请使用备份文件恢复数据库")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
