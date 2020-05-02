SELECT 
DATE(u.`createTime`) createTime,
u.`channelId` channelId,
a.`channelindex` channelindex,
a.`channelname` channelname,
COUNT(u.`userId`) registerNum,
COUNT(IF(u.`deductState`=1,u.`userId`,NULL)) cpaNum,
COUNT(IF(u.`deductState`=0,u.`userId`,NULL)) validNum
FROM partner.`t_channel_user` u JOIN partner.`t_channel_access` a ON a.`channelId`=u.`channelId`
WHERE u.`bindingType`=1
AND DATE(u.`createTime`) BETWEEN '{startTime}' AND '{endTime}'
AND IF('{channelname}'='',1=1,a.`channelname` LIKE '%{channelname}%')
AND IF('{channelindex}'='',1=1,a.`channelindex` LIKE '%{channelindex}%')
GROUP BY DATE(u.`createTime`),u.`channelId` HAVING registerNum<>0 ORDER BY u.`createTime` DESC LIMIT {rows};