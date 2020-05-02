#耗时较长，4 min左右

SELECT                                    
	a.`channelId` channelId,
	DATE(cu.`createTime`) accountingTime,             
	COUNT(DISTINCT cu.`userId`) registerNum,                            
	COUNT(DISTINCT IF(cu.`deductState`<>0, cu.`userId`, NULL)) cpaDeductNum,                           
	COUNT(DISTINCT IF(DATE(i.`investTime`) <= DATE_ADD(DATE(cu.`createTime`), INTERVAL 0 DAY), i.`investor`, NULL)) day1InvestNum,                   
	COUNT(DISTINCT IF(DATE(i.`investTime`) <= DATE_ADD(DATE(cu.`createTime`), INTERVAL 6 DAY), i.`investor`, NULL)) day7InvestNum,    
	COUNT(DISTINCT IF(DATE(i.`investTime`) <= DATE_ADD(DATE(cu.`createTime`), INTERVAL 29 DAY), i.`investor`, NULL)) day30InvestNum,              
	COUNT(DISTINCT IF(DATE(i.`investTime`) <= DATE_ADD(DATE(cu.`createTime`), INTERVAL 44 DAY), i.`investor`, NULL)) day45InvestNum,         
	COUNT(DISTINCT IF(DATE(i.`investTime`) <= DATE_ADD(DATE(cu.`createTime`), INTERVAL 89 DAY), i.`investor`, NULL)) day90InvestNum,            
	COUNT(DISTINCT IF(DATE(r.`createTime`) <= DATE_ADD(DATE(cu.`createTime`), INTERVAL 0 DAY), r.`userId`, NULL)) day1RechargeNum,       
	NOW() createTime,                       
	NOW() modifyTime,                             
	cu.`bindingType` bindingType
FROM partner.`t_channel_user` cu 
JOIN partner.`t_channel_access` a ON cu.`channelId`=a.`channelId` AND cu.`bindingType` IN (1,2,4,5)
LEFT JOIN product.`t_invest` i ON i.`investor`=cu.`userId` AND i.`result`=1
LEFT JOIN payment.`t_recharge_record` r ON r.`userId`=cu.`userId` AND r.`status`=0
GROUP BY DATE(cu.`createTime`), cu.`bindingType`, a.`channelId` ORDER BY channelId DESC, accountingTime DESC LIMIT {offset}, {limit};