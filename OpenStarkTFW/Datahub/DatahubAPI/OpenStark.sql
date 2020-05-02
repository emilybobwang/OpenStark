CREATE DATABASE IF NOT EXISTS Datahub DEFAULT CHARSET 'utf8';
USE Datahub;
CREATE TABLE IF NOT EXISTS `t_projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL COMMENT 'project 项目',
  `name` varchar(200) NOT NULL,
  `value` longtext NOT NULL,
  `status` smallint(1) NOT NULL DEFAULT '1' COMMENT '0 禁用, 1 正常',
  `createTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_t_projects_name` (`name`,`type`) USING BTREE,
  KEY `ix_t_projects_status` (`status`) USING HASH,
  KEY `ix_t_projects_createTime` (`createTime`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='项目信息表';

CREATE TABLE IF NOT EXISTS `t_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projectId` int(11) NOT NULL,
  `type` varchar(20) NOT NULL COMMENT 'txn 交易',
  `name` varchar(1000) NOT NULL,
  `value` longtext NOT NULL,
  `status` smallint(2) NOT NULL DEFAULT '1' COMMENT '0 禁用, 1 正常',
  `createTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `projectId` (`projectId`) USING HASH,
  KEY `ix_t_settings_type` (`type`) USING HASH,
  KEY `ix_t_settings_status` (`status`) USING HASH,
  KEY `createTime` (`createTime`) USING HASH,
  CONSTRAINT `t_settings_ibfk_1` FOREIGN KEY (`projectId`) REFERENCES `t_projects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='日志记录表';