SELECT 
u.`id` id,
u.`createTime` createTime, 
u.`userId` userId,
u.`username` username,
u.`mobile` mobile,
a.`channelname` channelname,
e.`realname` realname,
a.`channelPlatform` channelPlatform,
a.`channelDevice` channelDevice,
u.`channelId` channelId,
u.`deductDesc` deductDesc,
a.`creator` creator,
"system" dcCreator,
NULL bindingType
FROM partner.`t_channel_user` u JOIN partner.`t_channel_access` a ON a.`channelId`=u.`channelId`
LEFT JOIN partner.`t_channel_emp` e ON e.`id`=a.`channelEmpId`
JOIN partner.`t_channel_deduct_context` c ON c.`channelId`=u.`channelId`
WHERE u.`deductState` IN (1,2) AND u.`bindingType`=1
AND DATE(u.`createTime`) BETWEEN '{startTime}' AND '{endTime}'
AND IF('{channelname}'='',1=1,a.`channelname` LIKE '%{channelname}%')
AND IF('{username}'='',1=1,u.`username` LIKE '%{username}%')
AND IF('{mobile}'='',1=1,u.`mobile` LIKE '%{mobile}%')
GROUP BY u.`id` ORDER BY u.`id` DESC LIMIT {rows};