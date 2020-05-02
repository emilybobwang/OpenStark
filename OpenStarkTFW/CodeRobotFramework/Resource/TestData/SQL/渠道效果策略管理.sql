SELECT  
a.`authority` authority,
a.`channelCode` channelCode,
a.`channelDevice` channelDevice,
    (CASE a.`channelDevice`
        WHEN '1' THEN 'PC'                                                                                                                                                                                                   
        WHEN '2' THEN 'WAP'                                                                                                                                                                                                  
        WHEN '3' THEN '线下' 
        WHEN '4' THEN 'APP选项' 
        ELSE ''
    END)  channelDeviceDesc,
a.`channelGroup` channelGroup,
    (CASE a.`channelGroup`
        WHEN '1' THEN 'SNS推广'
        WHEN '2' THEN '渠道合作'
        WHEN '3' THEN '数字营销'
	WHEN '4' THEN '客户服务'
	WHEN '5'  THEN '移动推广'
	WHEN '6'  THEN '移动运营'
	WHEN '7'  THEN '品牌推广'
	WHEN '8'  THEN '其他'
	ELSE ''
     END)  channelGroupDesc,
a.`channelId` channelId,
a.`channelPlatform` channelPlatform,
NULL channelStateStr,
a.`channelSupplier` channelSupplier,
a.`channelindex` channelindex,
a.`channelname` channelname,
a.`channeltype` channeltype,
    (CASE a.`channeltype` 
        WHEN '1' THEN 'BD合作类'  #1BD合作类、2垂直媒体类、3品牌类、41效果类-DSP、42效果类-SEM、43效果类-其他、44效果类-信息流、45效果类-自媒体、5资源互换类                                                                  
        WHEN '2' THEN '垂直媒体类'                                                                                                                                                                                            
        WHEN '3' THEN '品牌类' 
        WHEN '7' THEN '效果类-应用市场'                                                                                                                                                                                                       
        WHEN '41' THEN '效果类-DSP'                                                                                                                                                                                           
        WHEN '42' THEN '效果类-SEM'                                                                                                                                                                                           
        WHEN '43' THEN '效果类-其他'                                                                                                                                                                                          
        WHEN '44' THEN '效果类-信息流'                                                                                                                                                                                        
        WHEN '45' THEN '效果类-自媒体'                                                                                                                                                                                        
        WHEN '5' THEN '资源互换类'  
        WHEN '6'  THEN '论坛贴吧类'    
        ELSE ''    
    END) channeltypeDesc,
IF(COUNT(DISTINCT u.`id`)=0,NULL,COUNT(DISTINCT u.`id`)) countNum,
a.`createTime` createTime,
a.`creator` creator,
c.`modifier` dcCreator,
CAST(c.`state` AS CHAR) dcState,
c.`deductConfig` deductConfig,
a.`detail` detail,
a.`groundingTime` groundingTime,
a.`hasReferee` hasReferee,
NULL hasRefereeStr,
a.`id` id,
a.`modifier` modifier,
c.`modifyTime` modifyTime,
NULL modifyTimeStr,
NULL name,
a.`parentChannelId` parentChannelId,
e.`realname` realname,
a.`rootChannelId` rootChannelId,
a.`state` state,
NULL dsState,
c.`id` contextId,
s.`deductModel` deductModel,
c.`deductType` deductType,
CAST(s.`id` AS CHAR) strategyId,
s.`name` strategyName
FROM partner.`t_channel_access` a 
LEFT JOIN partner.`t_channel_emp` e ON a.`channelEmpId`=e.`id`
JOIN partner.`t_channel_deduct_context` c ON c.`channelId`=a.`channelId`
JOIN partner.`t_channel_deduct_strategy` s ON s.`id`=c.`strategyId`
LEFT JOIN partner.`t_channel_user` u ON u.`channelId`=a.`channelId` AND u.`bindingType`=1 AND u.`deductState` <> 0
WHERE IF('{channelindex}'='',1=1,a.`channelindex` LIKE '%{channelindex}%') 
AND IF('{channelname}'='',1=1,a.`channelname` LIKE '%{channelname}%')
AND IF('{channelGroup}'='',1=1,a.`channelGroup` = '{channelGroup}')
AND IF('{channelPlatform}'='',1=1,a.`channelPlatform` LIKE '%{channelPlatform}%')
AND IF('{realname}'='',1=1,e.`realname` LIKE '%{realname}%')
GROUP BY a.`channelId`,s.`name` ORDER BY a.`channelId` DESC LIMIT {rows};
