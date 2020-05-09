LOCK TABLES `t_options` WRITE;
/*!40000 ALTER TABLE `t_options` DISABLE KEYS */;
INSERT INTO `t_options` VALUES (1,'cate','帮助','{\"upName\": \"\", \"upId\": \"\"}',1,'2020-05-08 08:30:03'),(2,'cate','开放接口','{\"upName\": \"帮助\", \"upId\": 1}',1,'2020-05-08 08:30:03');
/*!40000 ALTER TABLE `t_options` ENABLE KEYS */;
UNLOCK TABLES;