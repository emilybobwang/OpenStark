CREATE DATABASE IF NOT EXISTS OpenStark DEFAULT CHARSET 'utf8';
USE OpenStark;
CREATE TABLE IF NOT EXISTS `t_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `type` varchar(20) NOT NULL COMMENT 'active 动态, notice 通知, message 消息, todo 待办',
  `content` longtext NOT NULL,
  `status` smallint(1) NOT NULL DEFAULT '1' COMMENT '0 已删除 1 未读(未开始), 2 已读(进行中), 3 待完成, 4 马上到期, 5 已完成',
  `createTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `userId` (`userId`) USING HASH,
  KEY `type` (`type`) USING HASH,
  KEY `status` (`status`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='动态消息表';

CREATE TABLE IF NOT EXISTS `t_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL COMMENT 'common 通用, teams 团队, navLink 导航链接, cate 知识库分类',
  `name` varchar(255) NOT NULL,
  `value` longtext NOT NULL,
  `status` smallint(2) NOT NULL DEFAULT '1',
  `createTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_t_options_type_name` (`name`,`type`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='配置信息表(除项目相关以外的配置)';

CREATE TABLE IF NOT EXISTS `t_projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL COMMENT 'project 项目, tool 工具, sLoad 性能接口, env 环境, knowledge 知识库 [online 线上问题, book 文档]',
  `name` varchar(200) NOT NULL,
  `teamId` int(11) DEFAULT NULL,
  `config` longtext COMMENT '扩展配置 project[crypt 加解密、param 参数]',
  `status` smallint(1) NOT NULL DEFAULT '1' COMMENT '0 禁用, 1 正常',
  `createTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_t_projects_name` (`name`,`type`) USING BTREE,
  KEY `ix_t_projects_status` (`status`) USING HASH,
  KEY `ix_t_projects_teamId` (`teamId`) USING HASH,
  KEY `ix_t_projects_createTime` (`createTime`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='项目信息表';

CREATE TABLE IF NOT EXISTS `t_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projectId` int(11) NOT NULL,
  `type` varchar(20) NOT NULL COMMENT 'url 接口, env 环境详情, job 功能测试任务, jobG 自动化测试任务, jobA 接口测试任务, case 功能测试用例, caseG 自动化测试用例, caseA 接口测试用例, suite 功能测试集, suiteG 自动化测试集, suiteA 接口测试集, report 功能测试报告, reportG 自动化测试报告, reportA 接口测试报告',
  `name` varchar(1000) NOT NULL,
  `value` longtext NOT NULL,
  `status` smallint(2) NOT NULL DEFAULT '1' COMMENT '0 禁用, 1 正常, case[0 已废弃, 1 开发中, 2 已实现自动化测试, 3 已实现接口测试, 4 已实现自动化和接口测试], job[0 计划中, 1 排队中, 2 测试中, 3 已完成, 4 暂停, 5 异常]',
  `sort` smallint(11) NOT NULL DEFAULT '0',
  `createTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `projectId` (`projectId`) USING HASH,
  KEY `ix_t_settings_type` (`type`) USING HASH,
  KEY `ix_t_settings_status` (`status`) USING HASH,
  KEY `createTime` (`createTime`) USING HASH,
  CONSTRAINT `t_settings_ibfk_1` FOREIGN KEY (`projectId`) REFERENCES `t_projects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='项目相关配置信息表';

CREATE TABLE IF NOT EXISTS `t_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL DEFAULT '0',
  `projectId` int(11) NOT NULL DEFAULT '0',
  `type` varchar(20) NOT NULL COMMENT 'pv 访问量, active 活动量, load 性能',
  `name` varchar(255) NOT NULL,
  `value` longtext NOT NULL,
  `status` smallint(2) NOT NULL DEFAULT '1' COMMENT '0 失效, 1 有效',
  `createTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `projectId` (`projectId`) USING HASH,
  KEY `type` (`type`) USING HASH,
  KEY `status` (`status`) USING HASH,
  KEY `createTime` (`createTime`) USING HASH,
  KEY `userId` (`userId`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='测试活动统计报表';

CREATE TABLE IF NOT EXISTS `t_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(60) DEFAULT '',
  `password` varchar(255) NOT NULL DEFAULT '',
  `realname` varchar(50) DEFAULT '',
  `email` varchar(100) NOT NULL DEFAULT '',
  `profile` longtext,
  `role` smallint(1) NOT NULL DEFAULT '1' COMMENT '0 管理员, 1 普通用户',
  `status` smallint(1) NOT NULL DEFAULT '1' COMMENT '0 禁用, 1 未激活 , 2 正常',
  `registerTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lastLoginTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_t_users_email` (`email`) USING HASH,
  UNIQUE KEY `ix_t_users_username` (`username`) USING HASH,
  KEY `ix_t_users_status` (`status`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户信息表';