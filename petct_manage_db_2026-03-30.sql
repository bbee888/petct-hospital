# ************************************************************
# Sequel Ace SQL dump
# 版本号： 20099
#
# https://sequel-ace.com/
# https://github.com/Sequel-Ace/Sequel-Ace
#
# 主机: 127.0.0.1 (MySQL 9.6.0)
# 数据库: petct_manage_db
# 生成时间: 2026-03-29 16:23:09 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE='NO_AUTO_VALUE_ON_ZERO', SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# 转储表 appointments
# ------------------------------------------------------------

DROP TABLE IF EXISTS `appointments`;

CREATE TABLE `appointments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_domain` varchar(255) NOT NULL,
  `hospital_id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `idcard` varchar(30) NOT NULL,
  `sex` varchar(10) NOT NULL,
  `appoint_date` date NOT NULL,
  `intro` varchar(200) DEFAULT NULL COMMENT '病情介绍',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_app_domain` (`site_domain`),
  KEY `fk_app_hosp` (`hospital_id`),
  CONSTRAINT `fk_app_hosp` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# 转储表 article_categories
# ------------------------------------------------------------

DROP TABLE IF EXISTS `article_categories`;

CREATE TABLE `article_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_domain` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '站点域名（如：petct.com）',
  `name` varchar(100) NOT NULL COMMENT '分类名称',
  `slug` varchar(100) NOT NULL COMMENT '分类标识',
  PRIMARY KEY (`id`),
  KEY `idx_cat_domain` (`site_domain`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `article_categories` WRITE;
/*!40000 ALTER TABLE `article_categories` DISABLE KEYS */;

INSERT INTO `article_categories` (`id`, `site_domain`, `name`, `slug`)
VALUES
	(1,'www.ipetct.com','PETCT检查','petctjc'),
	(2,'www.ipetct.com','PETMR检查','petmrjc'),
	(3,'www.petctw.com','医院新闻','yynews');

/*!40000 ALTER TABLE `article_categories` ENABLE KEYS */;
UNLOCK TABLES;


# 转储表 article_tags
# ------------------------------------------------------------

DROP TABLE IF EXISTS `article_tags`;

CREATE TABLE `article_tags` (
  `article_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`article_id`,`tag_id`),
  KEY `idx_tag` (`tag_id`),
  KEY `idx_article_tag` (`article_id`,`tag_id`),
  CONSTRAINT `fk_at_art` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_at_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# 转储表 articles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `articles`;

CREATE TABLE `articles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL COMMENT '分类ID',
  `title` varchar(100) NOT NULL COMMENT '文章标题',
  `tags` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'tags',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'SEO描述',
  `content` text NOT NULL COMMENT '文章内容',
  `cover` varchar(100) DEFAULT NULL COMMENT '文章封面（URL）',
  `view_count` int DEFAULT '0' COMMENT '访问量',
  `is_published` tinyint DEFAULT '0' COMMENT '是否发布（1：已发布，0：未发布）',
  `published_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  PRIMARY KEY (`id`),
  KEY `fk_art_cat` (`category_id`),
  CONSTRAINT `fk_art_cat` FOREIGN KEY (`category_id`) REFERENCES `article_categories` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;

INSERT INTO `articles` (`id`, `category_id`, `title`, `tags`, `description`, `content`, `cover`, `view_count`, `is_published`, `published_at`)
VALUES
	(1,3,'武汉增驾A2驾校 武汉考A2拖头半挂驾照招生','','','<h5>武汉增驾A2驾校 武汉考A2拖头半挂驾照招生</h5>','',35,0,'2026-03-16 13:27:26');

/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;


# 转储表 categories
# ------------------------------------------------------------

DROP TABLE IF EXISTS `categories`;

CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `site_domain` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_categories_slug` (`slug`),
  KEY `ix_categories_site_domain` (`site_domain`),
  KEY `ix_categories_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# 转储表 cities
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cities`;

CREATE TABLE `cities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `province_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_city_prov` (`province_id`),
  CONSTRAINT `fk_city_prov` FOREIGN KEY (`province_id`) REFERENCES `provinces` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `cities` WRITE;
/*!40000 ALTER TABLE `cities` DISABLE KEYS */;

INSERT INTO `cities` (`id`, `province_id`, `name`)
VALUES
	(1,4,'黄浦区'),
	(2,4,'徐汇区'),
	(3,4,'长宁区'),
	(4,4,'静安区'),
	(5,4,'普陀区'),
	(6,4,'虹口区'),
	(7,4,'杨浦区'),
	(8,4,'闵行区'),
	(9,4,'宝山区'),
	(10,4,'嘉定区'),
	(11,4,'浦东新区'),
	(12,4,'金山区'),
	(13,4,'松江区'),
	(14,4,'青浦区'),
	(15,4,'奉贤区'),
	(16,4,'崇明区'),
	(17,5,'东城区'),
	(18,5,'西城区'),
	(19,5,'朝阳区'),
	(20,5,'丰台区'),
	(21,5,'石景山区'),
	(22,5,'海淀区'),
	(23,5,'门头沟区'),
	(24,5,'房山区'),
	(25,5,'通州区'),
	(26,5,'顺义区'),
	(27,5,'昌平区'),
	(28,5,'大兴区'),
	(29,5,'怀柔区'),
	(30,5,'平谷区'),
	(31,5,'密云区'),
	(32,5,'延庆区'),
	(33,6,'和平区'),
	(34,6,'河东区'),
	(35,6,'河西区'),
	(36,6,'南开区'),
	(37,6,'河北区'),
	(38,6,'红桥区'),
	(39,6,'东丽区'),
	(40,6,'西青区'),
	(41,6,'津南区'),
	(42,6,'北辰区'),
	(43,6,'武清区'),
	(44,6,'宝坻区'),
	(45,6,'滨海新区'),
	(46,6,'宁河区'),
	(47,6,'静海区'),
	(48,6,'蓟州区'),
	(49,7,'万州区'),
	(50,7,'涪陵区'),
	(51,7,'渝中区'),
	(52,7,'大渡口区'),
	(53,7,'江北区'),
	(54,7,'沙坪坝区'),
	(55,7,'九龙坡区'),
	(56,7,'南岸区'),
	(57,7,'北碚区'),
	(58,7,'綦江区'),
	(59,7,'大足区'),
	(60,7,'渝北区'),
	(61,7,'巴南区'),
	(62,7,'黔江区'),
	(63,7,'长寿区'),
	(64,7,'江津区'),
	(65,7,'合川区'),
	(66,7,'永川区'),
	(67,7,'南川区'),
	(68,7,'璧山区'),
	(69,7,'铜梁区'),
	(70,7,'潼南区'),
	(71,7,'荣昌区'),
	(72,7,'开州区'),
	(73,7,'梁平区'),
	(74,7,'武隆区'),
	(75,7,'城口县'),
	(76,7,'丰都县'),
	(77,7,'垫江县'),
	(78,7,'忠县'),
	(79,7,'云阳县'),
	(80,7,'奉节县'),
	(81,7,'巫山县'),
	(82,7,'巫溪县'),
	(83,8,'石家庄市'),
	(84,8,'唐山市'),
	(85,8,'秦皇岛市'),
	(86,8,'邯郸市'),
	(87,8,'邢台市'),
	(88,8,'保定市'),
	(89,8,'张家口市'),
	(90,8,'承德市'),
	(91,8,'沧州市'),
	(92,8,'廊坊市'),
	(93,8,'衡水市'),
	(94,9,'太原市'),
	(95,9,'大同市'),
	(96,9,'阳泉市'),
	(97,9,'长治市'),
	(98,9,'晋城市'),
	(99,9,'朔州市'),
	(100,9,'晋中市'),
	(101,9,'运城市'),
	(102,9,'忻州市'),
	(103,9,'临汾市'),
	(104,9,'吕梁市'),
	(105,10,'呼和浩特市'),
	(106,10,'包头市'),
	(107,10,'乌海市'),
	(108,10,'赤峰市'),
	(109,10,'通辽市'),
	(110,10,'鄂尔多斯市'),
	(111,10,'呼伦贝尔市'),
	(112,10,'巴彦淖尔市'),
	(113,10,'乌兰察布市'),
	(114,10,'兴安盟'),
	(115,10,'锡林郭勒盟'),
	(116,10,'阿拉善盟'),
	(117,11,'沈阳市'),
	(118,11,'大连市'),
	(119,11,'鞍山市'),
	(120,11,'抚顺市'),
	(121,11,'本溪市'),
	(122,11,'丹东市'),
	(123,11,'锦州市'),
	(124,11,'营口市'),
	(125,11,'阜新市'),
	(126,11,'辽阳市'),
	(127,11,'盘锦市'),
	(128,11,'铁岭市'),
	(129,11,'朝阳市'),
	(130,11,'葫芦岛市'),
	(131,12,'长春市'),
	(132,12,'吉林市'),
	(133,12,'四平市'),
	(134,12,'辽源市'),
	(135,12,'通化市'),
	(136,12,'白山市'),
	(137,12,'松原市'),
	(138,12,'白城市'),
	(139,12,'延边朝鲜族自治州'),
	(140,13,'哈尔滨市'),
	(141,13,'齐齐哈尔市'),
	(142,13,'鸡西市'),
	(143,13,'鹤岗市'),
	(144,13,'双鸭山市'),
	(145,13,'大庆市'),
	(146,13,'伊春市'),
	(147,13,'佳木斯市'),
	(148,13,'七台河市'),
	(149,13,'牡丹江市'),
	(150,13,'黑河市'),
	(151,13,'绥化市'),
	(152,13,'大兴安岭地区'),
	(153,14,'南京市'),
	(154,14,'无锡市'),
	(155,14,'徐州市'),
	(156,14,'常州市'),
	(157,14,'苏州市'),
	(158,14,'南通市'),
	(159,14,'连云港市'),
	(160,14,'淮安市'),
	(161,14,'盐城市'),
	(162,14,'扬州市'),
	(163,14,'镇江市'),
	(164,14,'泰州市'),
	(165,14,'宿迁市'),
	(166,15,'杭州市'),
	(167,15,'宁波市'),
	(168,15,'温州市'),
	(169,15,'嘉兴市'),
	(170,15,'湖州市'),
	(171,15,'绍兴市'),
	(172,15,'金华市'),
	(173,15,'衢州市'),
	(174,15,'舟山市'),
	(175,15,'台州市'),
	(176,15,'丽水市'),
	(177,16,'合肥市'),
	(178,16,'芜湖市'),
	(179,16,'蚌埠市'),
	(180,16,'淮南市'),
	(181,16,'马鞍山市'),
	(182,16,'淮北市'),
	(183,16,'铜陵市'),
	(184,16,'安庆市'),
	(185,16,'黄山市'),
	(186,16,'滁州市'),
	(187,16,'阜阳市'),
	(188,16,'宿州市'),
	(189,16,'六安市'),
	(190,16,'亳州市'),
	(191,16,'池州市'),
	(192,16,'宣城市'),
	(193,17,'福州市'),
	(194,17,'厦门市'),
	(195,17,'莆田市'),
	(196,17,'三明市'),
	(197,17,'泉州市'),
	(198,17,'漳州市'),
	(199,17,'南平市'),
	(200,17,'龙岩市'),
	(201,17,'宁德市'),
	(202,18,'南昌市'),
	(203,18,'景德镇市'),
	(204,18,'萍乡市'),
	(205,18,'九江市'),
	(206,18,'新余市'),
	(207,18,'鹰潭市'),
	(208,18,'赣州市'),
	(209,18,'吉安市'),
	(210,18,'宜春市'),
	(211,18,'抚州市'),
	(212,18,'上饶市'),
	(213,19,'济南市'),
	(214,19,'青岛市'),
	(215,19,'淄博市'),
	(216,19,'枣庄市'),
	(217,19,'东营市'),
	(218,19,'烟台市'),
	(219,19,'潍坊市'),
	(220,19,'济宁市'),
	(221,19,'泰安市'),
	(222,19,'威海市'),
	(223,19,'日照市'),
	(224,19,'临沂市'),
	(225,19,'德州市'),
	(226,19,'聊城市'),
	(227,19,'滨州市'),
	(228,19,'菏泽市'),
	(229,20,'郑州市'),
	(230,20,'开封市'),
	(231,20,'洛阳市'),
	(232,20,'平顶山市'),
	(233,20,'安阳市'),
	(234,20,'鹤壁市'),
	(235,20,'新乡市'),
	(236,20,'焦作市'),
	(237,20,'濮阳市'),
	(238,20,'许昌市'),
	(239,20,'漯河市'),
	(240,20,'三门峡市'),
	(241,20,'南阳市'),
	(242,20,'商丘市'),
	(243,20,'信阳市'),
	(244,20,'周口市'),
	(245,20,'驻马店市'),
	(246,20,'济源市'),
	(247,21,'武汉市'),
	(248,21,'黄石市'),
	(249,21,'十堰市'),
	(250,21,'宜昌市'),
	(251,21,'襄阳市'),
	(252,21,'鄂州市'),
	(253,21,'荆门市'),
	(254,21,'孝感市'),
	(255,21,'荆州市'),
	(256,21,'黄冈市'),
	(257,21,'咸宁市'),
	(258,21,'随州市'),
	(259,21,'恩施土家族苗族自治州'),
	(260,21,'仙桃市'),
	(261,21,'潜江市'),
	(262,21,'天门市'),
	(263,21,'神农架林区'),
	(264,22,'长沙市'),
	(265,22,'株洲市'),
	(266,22,'湘潭市'),
	(267,22,'衡阳市'),
	(268,22,'邵阳市'),
	(269,22,'岳阳市'),
	(270,22,'常德市'),
	(271,22,'张家界市'),
	(272,22,'益阳市'),
	(273,22,'郴州市'),
	(274,22,'永州市'),
	(275,22,'怀化市'),
	(276,22,'娄底市'),
	(277,22,'湘西土家族苗族自治州'),
	(278,23,'广州市'),
	(279,23,'韶关市'),
	(280,23,'深圳市'),
	(281,23,'珠海市'),
	(282,23,'汕头市'),
	(283,23,'佛山市'),
	(284,23,'江门市'),
	(285,23,'湛江市'),
	(286,23,'茂名市'),
	(287,23,'肇庆市'),
	(288,23,'惠州市'),
	(289,23,'梅州市'),
	(290,23,'汕尾市'),
	(291,23,'河源市'),
	(292,23,'阳江市'),
	(293,23,'清远市'),
	(294,23,'东莞市'),
	(295,23,'中山市'),
	(296,23,'潮州市'),
	(297,23,'揭阳市'),
	(298,23,'云浮市'),
	(299,24,'南宁市'),
	(300,24,'柳州市'),
	(301,24,'桂林市'),
	(302,24,'梧州市'),
	(303,24,'北海市'),
	(304,24,'防城港市'),
	(305,24,'钦州市'),
	(306,24,'贵港市'),
	(307,24,'玉林市'),
	(308,24,'百色市'),
	(309,24,'贺州市'),
	(310,24,'河池市'),
	(311,24,'来宾市'),
	(312,24,'崇左市'),
	(313,25,'海口市'),
	(314,25,'三亚市'),
	(315,25,'三沙市'),
	(316,25,'儋州市'),
	(317,25,'五指山市'),
	(318,25,'琼海市'),
	(319,25,'文昌市'),
	(320,25,'万宁市'),
	(321,25,'东方市'),
	(322,26,'成都市'),
	(323,26,'自贡市'),
	(324,26,'攀枝花市'),
	(325,26,'泸州市'),
	(326,26,'德阳市'),
	(327,26,'绵阳市'),
	(328,26,'广元市'),
	(329,26,'遂宁市'),
	(330,26,'内江市'),
	(331,26,'乐山市'),
	(332,26,'南充市'),
	(333,26,'眉山市'),
	(334,26,'宜宾市'),
	(335,26,'广安市'),
	(336,26,'达州市'),
	(337,26,'雅安市'),
	(338,26,'巴中市'),
	(339,26,'资阳市'),
	(340,26,'阿坝藏族羌族自治州'),
	(341,26,'甘孜藏族自治州'),
	(342,26,'凉山彝族自治州'),
	(343,27,'贵阳市'),
	(344,27,'六盘水市'),
	(345,27,'遵义市'),
	(346,27,'安顺市'),
	(347,27,'毕节市'),
	(348,27,'铜仁市'),
	(349,27,'黔西南布依族苗族自治州'),
	(350,27,'黔东南苗族侗族自治州'),
	(351,27,'黔南布依族苗族自治州'),
	(352,28,'昆明市'),
	(353,28,'曲靖市'),
	(354,28,'玉溪市'),
	(355,28,'保山市'),
	(356,28,'昭通市'),
	(357,28,'丽江市'),
	(358,28,'普洱市'),
	(359,28,'临沧市'),
	(360,28,'楚雄彝族自治州'),
	(361,28,'红河哈尼族彝族自治州'),
	(362,28,'文山壮族苗族自治州'),
	(363,28,'西双版纳傣族自治州'),
	(364,28,'大理白族自治州'),
	(365,28,'德宏傣族景颇族自治州'),
	(366,28,'怒江傈僳族自治州'),
	(367,28,'迪庆藏族自治州'),
	(368,29,'拉萨市'),
	(369,29,'日喀则市'),
	(370,29,'昌都市'),
	(371,29,'林芝市'),
	(372,29,'山南市'),
	(373,29,'那曲市'),
	(374,29,'阿里地区'),
	(375,30,'西安市'),
	(376,30,'铜川市'),
	(377,30,'宝鸡市'),
	(378,30,'咸阳市'),
	(379,30,'渭南市'),
	(380,30,'延安市'),
	(381,30,'汉中市'),
	(382,30,'榆林市'),
	(383,30,'安康市'),
	(384,30,'商洛市'),
	(385,31,'兰州市'),
	(386,31,'嘉峪关市'),
	(387,31,'金昌市'),
	(388,31,'白银市'),
	(389,31,'天水市'),
	(390,31,'武威市'),
	(391,31,'张掖市'),
	(392,31,'平凉市'),
	(393,31,'酒泉市'),
	(394,31,'庆阳市'),
	(395,31,'定西市'),
	(396,31,'陇南市'),
	(397,31,'临夏回族自治州'),
	(398,31,'甘南藏族自治州'),
	(399,32,'西宁市'),
	(400,32,'海东市'),
	(401,32,'海北藏族自治州'),
	(402,32,'黄南藏族自治州'),
	(403,32,'海南藏族自治州'),
	(404,32,'果洛藏族自治州'),
	(405,32,'玉树藏族自治州'),
	(406,32,'海西蒙古族藏族自治州'),
	(407,33,'银川市'),
	(408,33,'石嘴山市'),
	(409,33,'吴忠市'),
	(410,33,'固原市'),
	(411,33,'中卫市'),
	(412,34,'乌鲁木齐市'),
	(413,34,'克拉玛依市'),
	(414,34,'吐鲁番市'),
	(415,34,'哈密市'),
	(416,34,'昌吉回族自治州'),
	(417,34,'博尔塔拉蒙古自治州'),
	(418,34,'巴音郭楞蒙古自治州'),
	(419,34,'阿克苏地区'),
	(420,34,'克孜勒苏柯尔克孜自治州'),
	(421,34,'喀什地区'),
	(422,34,'和田地区'),
	(423,34,'伊犁哈萨克自治州'),
	(424,34,'塔城地区'),
	(425,34,'阿勒泰地区'),
	(426,34,'石河子市'),
	(427,34,'阿拉尔市'),
	(428,34,'图木舒克市'),
	(429,34,'五家渠市'),
	(430,34,'北屯市'),
	(431,34,'铁门关市'),
	(432,34,'双河市'),
	(433,34,'可克达拉市'),
	(434,34,'昆玉市'),
	(435,34,'胡杨河市');

/*!40000 ALTER TABLE `cities` ENABLE KEYS */;
UNLOCK TABLES;


# 转储表 districts
# ------------------------------------------------------------

DROP TABLE IF EXISTS `districts`;

CREATE TABLE `districts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city_id` int NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `city_id` (`city_id`),
  KEY `ix_districts_id` (`id`),
  CONSTRAINT `districts_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



# 转储表 hospital_tags
# ------------------------------------------------------------

DROP TABLE IF EXISTS `hospital_tags`;

CREATE TABLE `hospital_tags` (
  `hospital_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`hospital_id`,`tag_id`),
  KEY `idx_tag` (`tag_id`),
  KEY `idx_hospital_tag` (`hospital_id`,`tag_id`),
  CONSTRAINT `fk_ht_hosp` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_ht_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# 转储表 hospitals
# ------------------------------------------------------------

DROP TABLE IF EXISTS `hospitals`;

CREATE TABLE `hospitals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '医院名称',
  `province_id` int NOT NULL COMMENT '省份',
  `city_id` int NOT NULL COMMENT '城市ID',
  `level` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '医院等级',
  `price` int NOT NULL COMMENT '预约价格',
  `device` varchar(50) DEFAULT NULL COMMENT '设备型号',
  `address` varchar(100) DEFAULT NULL COMMENT '医院地址',
  `advantage` text COMMENT '医院优势',
  `ks_intro` text COMMENT '科室介绍',
  `content` text NOT NULL COMMENT '医院详情',
  `cover` varchar(200) DEFAULT NULL COMMENT '医院封面（URL）',
  `view_count` int DEFAULT '0' COMMENT '访问量',
  `is_published` tinyint DEFAULT '0' COMMENT '是否发布（1：已发布，0：未发布）',
  `create_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  `seo_title` varchar(100) DEFAULT NULL COMMENT 'SEO标题',
  `tags` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'tags',
  `seo_description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'SEO描述',
  `is_cooperation` tinyint(1) DEFAULT '0' COMMENT '默认0,合作医院1',
  PRIMARY KEY (`id`),
  KEY `fk_hosp_city` (`city_id`),
  KEY `fk_hosp_provice` (`province_id`),
  CONSTRAINT `fk_hosp_city` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `hospitals` WRITE;
/*!40000 ALTER TABLE `hospitals` DISABLE KEYS */;

INSERT INTO `hospitals` (`id`, `title`, `province_id`, `city_id`, `level`, `price`, `device`, `address`, `advantage`, `ks_intro`, `content`, `cover`, `view_count`, `is_published`, `create_at`, `seo_title`, `tags`, `seo_description`, `is_cooperation`)
VALUES
	(1,'上海华山医院PETCT中心',4,2,'综合医院',5300,'上海华山医院PETCT中心','上海华山医院PETCT中心','复旦大学附属华山医院PET中心于1996年由核医学科提出申请并做了技术方案论证，经院部批准报市卫生问题局，1997年3月国家卫生部批准立项。1998年12月15日完成第一例18F-FDG PET全身检查，1999年10月完成全国加速器的安装调试。PET仪为Siemens Biograph 64 HD，医用小型回旋加速器为美国CTI RDS III型及正电子放射性药物自动合成装置，是国内首批经卫生部批准引进并建成的PET中心之一。','<p><span style=\"color: rgb(33, 37, 41); background-color: rgb(255, 255, 255);\">上海华山医院PETCT中心</span></p>','<p><span style=\"color: rgb(33, 37, 41); background-color: rgb(255, 255, 255);\">上海华山医院PETCT中心</span><img src=\"http://localhost:8001/uploads/bd536120-52b5-4b5b-8b15-76db13254939.jpg\" alt=\"image\" data-href=\"http://localhost:8001/uploads/bd536120-52b5-4b5b-8b15-76db13254939.jpg\" style=\"\"/></p>','http://localhost:8001/uploads/18aaef90-f5c2-4a0a-b1b1-855c4ba5b377.jpg',52,0,'2026-03-16 08:12:11','上海华山医院_上海PETCT中心','上海华山医院,PETCT中心','上海华山医院PETCT中心',0),
	(2,'上海全景医学影像诊断(徐汇)中心',4,2,'影像中心',6500,'Siemens Biograph 64 HD','上海市徐汇区桂林路406号华鑫中心8号楼','上海全景医学影像诊断中心由国家卫计委批准成立，是一家以专业医学影像诊断为主要技术支撑，以肿瘤、心脑血管疾病、神经系统疾病等专病筛查为主要服务内容，同时开展精准影像扫描及诊断、深度健康体检、私人订制的专属医疗健康管家(健康档案管理、医学专家咨询、三甲医院就医协助等)等创新医疗服务的创新型、复合型连锁医疗机构。','','<p style=\"text-align: start;\">　　上海全景医学影像诊断中心由国家卫计委批准成立，是一家以专业医学影像诊断为主要技术支撑，以肿瘤、心脑血管疾病、神经系统疾病等专病筛查为主要服务内容，同时开展精准影像扫描及诊断、深度健康体检、私人订制的专属医疗健康管家(健康档案管理、医学专家咨询、三甲医院就医协助等)等创新医疗服务的创新型、复合型连锁医疗机构。上海全景是国内首家独立医学影像诊断中心，是精准影像的先行者、深度健检的实践者、专属医疗的提供者，也是亚太地区颇具规模的专业医学影像诊断机构。配备全球顶尖的影像设备</p><p style=\"text-align: start;\">　　SIEMENS Biograph mMR 正电子发射及磁共振成像系统</p><p style=\"text-align: start;\">　　上海第一台PET-MR(研究型)中心拥有全套从西门子引进的PET/MR(研究型)、Flash双源CT、PET/CT、3.0TMRI、1.5TMRI等全套高端医学影像设备，其影像诊断综合技术水平可与欧美日顶尖专业健检机构相比肩。其中的研究型PET/MR是现在全球最尖端的用于肿瘤筛查和诊断的医学影像设备，中国大陆地区目前仅配备两台，另一台在北京301医院，专门用于高层领导人健康体检。汇聚国内知名的影像专家中心拥有一支由影像医学泰斗周康荣教授、杨春山教授、肖湘生教授、高欣博士等知名专家领衔，并联合国际权威医学影像专家，组建而成的百余人的专业技术团队。</p><p style=\"text-align: start;\">　　影像医学泰斗——周康荣教授 指导分析影像报告执行国际严苛的质量管理体系中心执行国际严苛的质量管理体系，采用专业系统分组、三级报告审核制度、医生巡回上机扫描制度，打造国际化精准医学检测标准，为临床提供专业的诊断依据，提供国际品质的精准医学服务。周康荣教授指导分析影像诊断报告</p><p style=\"text-align: start;\">　　石华铮主任分析影像诊断报告提供高端绿色深度健检服务中心创立多种专病筛查方案，为客户提供高端绿色深度健检服务，如全身肿瘤绿色筛查、肺部肿瘤筛查、乳腺肿瘤筛查、冠心病筛查及风险评估方案等等。以肺癌为例：采用高分辨率靶扫描+三维重建技术使其初诊准确率由80%提高到98%以上;以乳腺癌为例：采用多种影像检查结合临床将其诊断准确率提高3倍。提供专属高端医疗服务50名医学博士组成的专家团为客户提供私人医生和就医规划;100家三甲医院直通绿色通道;全面对接200多名国内外著名医学专家。全景让健康有人管，看病不再难!牵手境内外优秀合作伙伴中心与国际第一家配备质子重离子放射治疗设备的上海市质子重离子医院、美国最好的医院之一的美国梅奥诊所、在线医疗咨询服务的领导者USARAD、世界著名的癌症治疗公司康铠士等行业精英携手合作，搭建国际医疗优质资源的桥梁，提供国际优质医疗服务。中心在医学影像诊断上本着安全、专业、精准的原则，在服务品质上追求完美和卓越，也致力打造温馨、优雅、洁净的环境，让客户既能享受到全球领先的健检服务，又能有一个安心、轻送、舒适的体检之旅。</p><p style=\"text-align: start;\">　　中心隶属于上海全景医学影像科技股份有限公司。随着上海、杭州、广州、重庆医学影像诊断中心及门诊部的相继运营，北京、武汉、成都、西安等地的布局，全景将在2020年前形成不少于8家的医学影像中心及门诊部并辐射周边，同时运用现代技术将大多数县域以上的医疗机构进行连接，形成国内广覆盖、宽领域、深层次的医学影像诊断及专属医疗服务网络，打造国内外知名的医学影像诊断品牌。</p>','http://localhost:8001/uploads/0df1d34f-b575-4a07-a017-8b52a17d5f50.jpg',11,0,'2026-03-16 17:26:41','上海全景医学影像诊断(徐汇)中心_上海全景医学影像中心','','上海全景医学影像诊断中心由国家卫计委批准成立，是一家以专业医学影像诊断为主要技术支撑，以肿瘤、心脑血管疾病、神经系统疾病等专病筛查为主要服务内容，同时开展精准影像扫描及诊断、深度健康体检、私人订制的专属医疗健康管家(健康档案管理、医学专家咨询、三甲医院就医协助等)等创新医疗服务的创新型、复合型连锁医疗机构。',0);

/*!40000 ALTER TABLE `hospitals` ENABLE KEYS */;
UNLOCK TABLES;


# 转储表 provinces
# ------------------------------------------------------------

DROP TABLE IF EXISTS `provinces`;

CREATE TABLE `provinces` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `provinces` WRITE;
/*!40000 ALTER TABLE `provinces` DISABLE KEYS */;

INSERT INTO `provinces` (`id`, `name`)
VALUES
	(4,'上海市'),
	(5,'北京市'),
	(6,'天津市'),
	(7,'重庆市'),
	(8,'河北省'),
	(9,'山西省'),
	(10,'内蒙古'),
	(11,'辽宁省'),
	(12,'吉林省'),
	(13,'黑龙江省'),
	(14,'江苏省'),
	(15,'浙江省'),
	(16,'安徽省'),
	(17,'福建省'),
	(18,'江西省'),
	(19,'山东省'),
	(20,'河南省'),
	(21,'湖北省'),
	(22,'湖南省'),
	(23,'广东省'),
	(24,'广西省'),
	(25,'海南省'),
	(26,'四川省'),
	(27,'贵州省'),
	(28,'云南省'),
	(29,'西藏'),
	(30,'陕西省'),
	(31,'甘肃省'),
	(32,'青海省'),
	(33,'宁夏'),
	(34,'新疆');

/*!40000 ALTER TABLE `provinces` ENABLE KEYS */;
UNLOCK TABLES;


# 转储表 sites
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sites`;

CREATE TABLE `sites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL COMMENT '站点域名（如：petct.com）',
  `name` varchar(100) NOT NULL COMMENT '站点名称（如：宠物CT中心）',
  `logo` varchar(500) DEFAULT NULL COMMENT '站点logo（URL）',
  `seo_title` varchar(100) DEFAULT NULL COMMENT 'SEO标题',
  `seo_keywords` varchar(120) DEFAULT NULL COMMENT 'SEO关键词',
  `seo_description` varchar(255) DEFAULT NULL COMMENT 'SEO描述',
  `status` tinyint DEFAULT '1' COMMENT '状态（1：正常，0：禁用）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `domain` (`domain`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `sites` WRITE;
/*!40000 ALTER TABLE `sites` DISABLE KEYS */;

INSERT INTO `sites` (`id`, `domain`, `name`, `logo`, `seo_title`, `seo_keywords`, `seo_description`, `status`, `created_at`)
VALUES
	(1,'www.ipetct.com','ipetct',NULL,'ipetct','ipetct','ipetct',1,'2026-03-16 06:02:33'),
	(2,'www.petct265.com','petct265',NULL,'','','',1,'2026-03-16 10:08:45'),
	(3,'www.petctw.com','petctw',NULL,'','','',1,'2026-03-16 10:09:07'),
	(4,'www.cnpetct.com','cnpetct',NULL,'','','',1,'2026-03-16 10:09:24'),
	(5,'www.yypetct.com','yypetct',NULL,'PETCT检查预约平台_癌症筛查_肿瘤复查_高端体检','petct检查,petct预约,petct医院,petct价格,petct中心,petct费用,什么是petct,核磁,高端体检','petct检查预约平台是一个综合性的petct检查预约网站,汇集全国三甲医院、专业影像中心等。为每位用户提供最方便省时的预约与咨询服务，直接医院交费，安全可靠。',1,'2026-03-17 00:21:28'),
	(6,'www.hupetct.com','hupetct',NULL,'上海PETCT线上预约平台','广州PETCT医院,广州PETCT检查,上海PETCT医院,上海PETCT检查,浙江PETCT医院,浙江PETCT检查,江苏PETCT医院,江苏PETCT检查,深圳PETCT检查,北京PETCT检查','上海PETCT预约平台是正规的PETCT在线检查预约平台。提供广州PETCT医院、深圳PETCT医院、上海PETCT医院、浙江PETCT医院、江苏PETCT医院、武汉PETCT医院、北京PETCT医院等地区PETCT医院预约信息。在线免费预约，去医院检查无须排队，医院交费，安全可靠。',1,'2026-03-17 00:23:12'),
	(7,'www.gdpetct.com','gdpetct',NULL,'广州PETCT医院检查预约中心_深圳|东莞|佛山|珠海|中山PETCT体检及癌症筛查','广州PETCT,广州PETCT医院,广州PETCT检查,广州PETCT预约,深圳PETCT医院,深圳PETCT,佛山PETCT,东莞PETCT,珠海PETCT,中山PETCT,广东PETCT医院,癌症筛查','广州PETCT预约网是广东地区正规的PETCT在线检查预约平台。提供广州PETCT医院、深圳PETCT医院、佛山PETCT医院、东莞PETCT医院、中山PETCT医院、惠州PETCT医院、珠海PETCT医院等地区PETCT医院预约信息。在线免费预约，去医院检查无须排队，医院交费，安全可靠。',1,'2026-03-17 00:24:02'),
	(8,'www.petctyy.com','petctyy',NULL,'petctyy','petctyy','petctyy',1,'2026-03-17 00:24:29'),
	(9,'www.yypetmr.com','yypetmr',NULL,'yypetmr','yypetmr','yypetmr',1,'2026-03-17 00:24:59'),
	(10,'www.petmr114.com','petmr114',NULL,'petmr114','petmr114','petmr114',1,'2026-03-17 00:26:08'),
	(11,'www.spetct.com','spetct',NULL,'spetct','spetct','spetct',0,'2026-03-17 00:26:48'),
	(12,'www.chayixun.com','chayixun',NULL,'chayixun','chayixun','chayixun',0,'2026-03-17 00:27:30'),
	(13,'www.whznyy.com','whznyy',NULL,'武汉大学中南医院','武汉大学中南医院,武汉中南医院','武汉大学中南医院',0,'2026-03-17 00:28:16'),
	(14,'www.hbchyy.com','hbchyy',NULL,'湖北肿瘤医院','湖北肿瘤医院','湖北肿瘤医院',0,'2026-03-17 00:29:07'),
	(15,'www.hbrmhospital.com','hbrmhospital',NULL,'湖北人民医院,武汉大学人民医院','湖北人民医院','湖北人民医院',0,'2026-03-17 00:31:12');

/*!40000 ALTER TABLE `sites` ENABLE KEYS */;
UNLOCK TABLES;


# 转储表 tags
# ------------------------------------------------------------

DROP TABLE IF EXISTS `tags`;

CREATE TABLE `tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `use_count` int DEFAULT '0' COMMENT '使用统计次数',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# 转储表 users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(30) DEFAULT NULL COMMENT '用户邮箱',
  `realname` varchar(30) DEFAULT NULL COMMENT '用户真实姓名',
  `is_active` tinyint DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`id`, `username`, `password_hash`, `email`, `realname`, `is_active`, `created_at`)
VALUES
	(1,'admin','$2b$12$EjmDUC5RHv3aCShrKDv5eOHtAiBAe/QTaYj.deRnFnKwFUbMn8V.G',NULL,NULL,1,'2026-03-16 05:31:22');

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
