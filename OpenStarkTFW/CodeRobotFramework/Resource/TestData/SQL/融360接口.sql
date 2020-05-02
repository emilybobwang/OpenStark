#融360注册数据接口
SELECT 
    cu.`username` userName,
    CONCAT(LEFT(cu.`mobile`,3),'****',RIGHT(cu.`mobile`,4)) mobile,
    DATE(cu.`createTime`) registerTime,
    CONCAT(CAST(re.`amount` AS DECIMAL(20,2)),'元') fristRechargeAmount,
    DATE(re.`createTime`) fristRechargeTime,
    NULL fristConsumeTime
FROM partner.`t_channel_user` cu 
LEFT JOIN partner.`t_channel_recharge_record` re
ON cu.`userId`=re.`userId` 
LEFT JOIN partner.`t_channel_invest` i
ON cu.`userId`=i.`userId`
WHERE cu.`channelId`='10001' AND cu.`deductState`=0 AND cu.`bindingType`=1 
AND cu.`createTime` BETWEEN '{startTime}' AND '{endTime}'
GROUP BY cu.`userId`
LIMIT {rows};