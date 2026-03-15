-- 创建数据库（如已存在可注释掉）
CREATE DATABASE IF NOT EXISTS petct_manage_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE petct_manage_db;

SET FOREIGN_KEY_CHECKS = 0;

-- 1. 用户表 (简化版：无角色，登录即管理员)
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL UNIQUE,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(30) DEFAULT NULL COMMENT '用户邮箱',
  `realname` varchar(30) DEFAULT NULL COMMENT '用户真实姓名',
  `is_active` tinyint DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO users (username, password_hash) VALUES ('admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'); 

-- 2. 站点表 (多租户核心)
CREATE TABLE IF NOT EXISTS `sites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL UNIQUE COMMENT '站点域名（如：petct.com）',
  `name` varchar(100) NOT NULL COMMENT '站点名称（如：宠物CT中心）',
  `logo` varchar(500) DEFAULT NULL COMMENT '站点logo（URL）',
  `seo_title` varchar(100) DEFAULT NULL COMMENT 'SEO标题',
  `seo_keywords` varchar(120) DEFAULT NULL COMMENT 'SEO关键词',
  `seo_description` varchar(255) DEFAULT NULL COMMENT 'SEO描述',
  `status` tinyint DEFAULT '1' COMMENT '状态（1：正常，0：禁用）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 基础地理信息
CREATE TABLE IF NOT EXISTS `provinces` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `cities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `province_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_city_prov` FOREIGN KEY (`province_id`) REFERENCES `provinces` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. 医院表 (带 domain 隔离)
CREATE TABLE IF NOT EXISTS `hospitals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_domain` varchar(255) NOT NULL COMMENT '站点域名（如：petct.com）',
  `city_id` int NOT NULL COMMENT '城市ID',
  `title` varchar(100) NOT NULL COMMENT '医院名称',
  `seo_keywords` varchar(200) COMMENT 'SEO关键词',
  `seo_description` varchar(255) COMMENT 'SEO描述',
  `price` int COMMENT '预约价格',
  `device` varchar(50) COMMENT '设备型号',
  `address` varchar(100) COMMENT '医院地址',
  `advantage` text COMMENT '医院优势',
  `ks_intro` text COMMENT '科室介绍',
  `content` text NOT NULL COMMENT '医院详情',
  `cover` varchar(200) COMMENT '医院封面（URL）',
  `view_count` int DEFAULT 0 COMMENT '访问量',
  `is_published` tinyint DEFAULT 0 COMMENT '是否发布（1：已发布，0：未发布）',
  `published_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  INDEX `idx_site_domain` (`site_domain`),
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_hosp_city` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. 文章分类与文章 (带 domain 隔离)
CREATE TABLE IF NOT EXISTS `article_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_domain` varchar(255) NOT NULL COMMENT '站点域名（如：petct.com）',
  `name` varchar(100) NOT NULL COMMENT '分类名称',
  `slug` varchar(100) NOT NULL COMMENT '分类标识',
  INDEX `idx_cat_domain` (`site_domain`),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `articles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_domain` varchar(255) NOT NULL COMMENT '站点域名（如：petct.com）',
  `category_id` int NOT NULL COMMENT '分类ID',
  `title` varchar(100) NOT NULL COMMENT '文章标题',
  `seo_keywords` varchar(120) COMMENT 'SEO关键词',
  `seo_description` varchar(255) COMMENT 'SEO描述',
  `content` text NOT NULL COMMENT '文章内容',
  `cover` varchar(100) COMMENT '文章封面（URL）',
  `view_count` int DEFAULT 0 COMMENT '访问量',
  `is_published` tinyint DEFAULT 0 COMMENT '是否发布（1：已发布，0：未发布）',
  `published_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  INDEX `idx_art_domain` (`site_domain`),
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_art_cat` FOREIGN KEY (`category_id`) REFERENCES `article_categories` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. 全局标签表 (核心：Name/Slug 全局唯一，不区分域名)
CREATE TABLE IF NOT EXISTS `tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL UNIQUE,
  `slug` varchar(50) NOT NULL UNIQUE,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. 关联表 (多对多)
CREATE TABLE IF NOT EXISTS `article_tags` (
  `article_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`article_id`, `tag_id`),
  INDEX `idx_tag` (`tag_id`),
  CONSTRAINT `fk_at_art` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_at_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `hospital_tags` (
  `hospital_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`hospital_id`, `tag_id`),
  INDEX `idx_tag` (`tag_id`),
  CONSTRAINT `fk_ht_hosp` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_ht_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. 预约表
CREATE TABLE IF NOT EXISTS `appointments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_domain` varchar(255) NOT NULL,
  `hospital_id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `idcard` varchar(30) NOT NULL,
  `sex` varchar(10) NOT NULL,
  `appoint_date` date NOT NULL,
  `intro` varchar(200) COMMENT '病情介绍',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint DEFAULT 0,
  INDEX `idx_app_domain` (`site_domain`),
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_app_hosp` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;