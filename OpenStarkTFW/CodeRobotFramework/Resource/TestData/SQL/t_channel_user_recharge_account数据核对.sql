#耗时较长，1 min左右
SELECT 
	cu.`userId` AS userId,
	DATE(cu.`registerTime`) AS registerTime,
	DATE(re.`createTime`) AS firstRechargeTime,
	CAST(re.`amount` AS DECIMAL(20,5)) AS firstRechargeAmount,
	CAST(SUM(IF(DATE(re.`createTime`) <= DATE_ADD(DATE(cu.`registerTime`), INTERVAL 0 DAY),re.`amount`, 0)) AS DECIMAL(20,5)) AS day1RechargeAmount,
	CAST(SUM(IF(DATE(re.`createTime`) <= DATE_ADD(DATE(cu.`registerTime`), INTERVAL 6 DAY),re.`amount`, 0)) AS DECIMAL(20,5)) AS day7RechargeAmount, 
	CAST(SUM(IF(DATE(re.`createTime`) <= DATE_ADD(DATE(cu.`registerTime`), INTERVAL 29 DAY),re.`amount`, 0)) AS DECIMAL(20,5)) AS day30RechargeAmount,
	CAST(SUM(IF(DATE(re.`createTime`) <= DATE_ADD(DATE(cu.`registerTime`), INTERVAL 44 DAY),re.`amount`, 0)) AS DECIMAL(20,5)) AS day45RechargeAmount,
	CAST(SUM(IF(DATE(re.`createTime`) <= DATE_ADD(DATE(cu.`registerTime`), INTERVAL 89 DAY),re.`amount`, 0)) AS DECIMAL(20,5)) AS day90RechargeAmount,
	CAST(SUM(re.`amount`) AS DECIMAL(20,5)) AS totalRechargeAmount, 
	COUNT(DISTINCT re.`txnId`) AS totalRechargeNum,
	NOW() AS createTime,	#时间仅参考，跟实际不一致
	NOW() AS modifyTime	#时间仅参考，跟实际不一致
FROM payment.`t_recharge_record` AS re 
JOIN (SELECT DISTINCT tcu.`userId` AS userId, tcu.`registerTime` FROM partner.`t_channel_user` AS tcu WHERE tcu.`bindingType` IN (1,2,4,5)) AS cu
ON cu.`userId` = re.`userId` AND re.`status`=0
GROUP BY cu.`userId` ORDER BY userId DESC LIMIT {offset}, {limit};  