#耗时较长，2 min左右
SELECT 
	u.`id` AS userId,                                    
	DATE(u.`createTime`) AS registerTime,                               
	IFNULL((SELECT LEAST(DATE(IFNULL(i.`investTime`,ip.createTime)), DATE(IFNULL(ip.createTime,i.`investTime`))) FROM pcts.t_invest AS ip RIGHT JOIN xnaccount.`t_user_person` up ON ip.`userId`=up.`id` LEFT JOIN product.`t_invest` AS i ON i.`investor`=up.`id` AND i.`result`=1 AND (i.`productType`<>12 OR i.`productType` IS NULL) AND i.`investAmount` <> 0 WHERE up.id=u.`id` order by ip.createTime,i.investTime LIMIT 1),NULL) AS firstInvestTime,    
	CAST(IFNULL((SELECT IF(i.investTime<ip.createTime,i.`investAmount`,ip.amount/100) FROM pcts.t_invest AS ip RIGHT JOIN xnaccount.`t_user_person` up ON ip.`userId`=up.`id` LEFT JOIN product.`t_invest` AS i ON i.`investor`=up.`id` AND i.`result`=1 AND (i.`productType`<>12 OR i.`productType` IS NULL) AND i.`investAmount` <> 0 WHERE up.id=u.`id` order by ip.createTime,i.investTime LIMIT 1), 0) AS DECIMAL(20,5)) AS firstInvestAmount,   
	COUNT(DISTINCT IF(i.`investAmount`<>0,i.id,NULL))+COUNT(DISTINCT ip.id) AS totalInvestNum,                 
	CAST(SUM(DISTINCT IF((i.`productType` NOT IN (11,12,13,15) OR i.`productType` IS NULL) AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 0 DAY), i.`investAmount`, 0))+SUM(IF(DATE(ip.`createTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 0 DAY),ip.amount/100,0)) AS DECIMAL(20,5)) AS day1RegularInvest,           
	CAST(SUM(DISTINCT IF((i.`productType` NOT IN (11,12,13,15) OR i.`productType` IS NULL) AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 6 DAY), i.`investAmount`, 0))+SUM(IF(DATE(ip.`createTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 6 DAY),ip.amount/100,0)) AS DECIMAL(20,5)) AS day7RegularInvest,       
	CAST(SUM(DISTINCT IF((i.`productType` NOT IN (11,12,13,15) OR i.`productType` IS NULL) AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 29 DAY), i.`investAmount`, 0))+SUM(IF(DATE(ip.`createTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 29 DAY),ip.amount/100,0)) AS DECIMAL(20,5)) AS day30RegularInvest,           
	CAST(SUM(DISTINCT IF((i.`productType` NOT IN (11,12,13,15) OR i.`productType` IS NULL) AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 44 DAY), i.`investAmount`, 0))+SUM(IF(DATE(ip.`createTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 44 DAY),ip.amount/100,0)) AS DECIMAL(20,5)) AS day45RegularInvest,    
	CAST(SUM(DISTINCT IF((i.`productType` NOT IN (11,12,13,15) OR i.`productType` IS NULL) AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 89 DAY), i.`investAmount`, 0))+SUM(IF(DATE(ip.`createTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 89 DAY),ip.amount/100,0)) AS DECIMAL(20,5)) AS day90RegularInvest,     
	CAST(SUM(DISTINCT IF((i.`productType` NOT IN (11,12,13,15) OR i.`productType` IS NULL), IFNULL(i.`investAmount`,0), 0))+SUM(ip.amount/100) AS DECIMAL(20,5)) AS totalRegularInvest,                    
	CAST(SUM(DISTINCT IF(i.`productType` IN (11,13,15) AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 0 DAY), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS day1CurrentInvest,          
	CAST(SUM(DISTINCT IF(i.`productType` IN (11,13,15) AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 6 DAY), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS day7CurrentInvest,   
	CAST(SUM(DISTINCT IF(i.`productType` IN (11,13,15) AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 29 DAY), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS day30CurrentInvest,      
	CAST(SUM(DISTINCT IF(i.`productType` IN (11,13,15) AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 44 DAY), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS day45CurrentInvest,  
	CAST(SUM(DISTINCT IF(i.`productType` IN (11,13,15) AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 89 DAY), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS day90CurrentInvest,    
	CAST(SUM(DISTINCT IF(i.`productType` IN (11,13,15), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS totalCurrentInvest,            
	CAST(SUM(DISTINCT IF(i.`productType`=12 AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 0 DAY), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS day1FinanceInvest,         
	CAST(SUM(DISTINCT IF(i.`productType`=12 AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 6 DAY), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS day7FinanceInvest,  
	CAST(SUM(DISTINCT IF(i.`productType`=12 AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 29 DAY), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS day30FinanceInvest, 
	CAST(SUM(DISTINCT IF(i.`productType`=12 AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 44 DAY), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS day45FinanceInvest,    
	CAST(SUM(DISTINCT IF(i.`productType`=12 AND DATE(i.`investTime`) <= DATE_ADD(DATE(u.`createTime`), INTERVAL 89 DAY), i.`investAmount`, 0)) AS DECIMAL(20,5)) AS day90FinanceInvest,     
	CAST(SUM(DISTINCT IF(i.`productType`=12, i.`investAmount`, 0)) AS DECIMAL(20,5)) AS totalFinanceInvest,             
	NOW() AS createTime,	#时间仅参考，跟实际不一致                              
	NOW() AS modifyTime    #时间仅参考，跟实际不一致      
FROM product.`t_invest` AS i
RIGHT JOIN xnaccount.`t_user_person` u ON i.`investor`=u.`id` AND i.`result`=1 
LEFT JOIN pcts.t_invest ip on ip.userId=u.id
WHERE u.`id` IN ({users})
GROUP BY u.`id` HAVING firstInvestTime is not NULL ORDER BY userId DESC LIMIT {offset}, {limit};
