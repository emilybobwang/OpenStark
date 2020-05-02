SELECT
	cu.`userId` userId,
	ca.`id` channelAccountId,
	cu.`bindingType` bindingType,
	cu.`deductState` deductState,
	NOW() createTime
FROM partner.`t_channel_user` cu 
JOIN partner.`t_channel_account` ca ON cu.`registerTime`=ca.`accountingTime` AND ca.`channelId`=cu.`channelId` AND ca.`bindingType`=cu.`bindingType`
WHERE cu.`bindingType` IN (1,2,4,5) AND (cu.`userId` IN (SELECT DISTINCT r.`userId` FROM payment.`t_recharge_record` r WHERE r.`status`=0)
OR cu.`userId` IN ({users})) 
ORDER BY cu.`userId` DESC LIMIT {offset}, {limit};
