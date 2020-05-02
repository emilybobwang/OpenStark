SELECT 
	'总计' firstInvestDate,
	NULL userName,
	SUM(tt.`investTimes`) investTimes,
	SUM(tt.`firstInvestAmount`) firstInvestAmount, 
	SUM(tt.`investAmountSum`) investAmountSum,
	SUM(tt.`currentAmountSum`) currentAmountSum,
	SUM(tt.`regularAmountSum`) regularAmountSum,
	SUM(tt.`financierAmountSum`) financierAmountSum,
	CONCAT(MIN(tt.`registerTime`),'--',MAX(tt.`registerTime`)) registerTime,
	NULL channelname,
    NULL channelEmpName,
	0 channeltype,
	NULL channeltypeDesc,
	NULL channelPlatform,
	0 channelDevice,
	NULL channelDeviceDesc,
	0 channelGroup,
	NULL channelGroupDesc,
	NULL channelMode,
	NULL channelModeDesc
FROM 
(SELECT 
    i.`firstInvestTime` firstInvestDate,
    CAST(IFNULL(i.`firstInvestAmount`,0)/10000 AS DECIMAL(10,4)) firstInvestAmount,
    c.`username` userName,
    IFNULL(i.`totalInvestNum`, 0) investTimes,
    CAST(IFNULL((i.`totalCurrentInvest` + i.`totalRegularInvest`), 0)/10000 AS DECIMAL(10,4)) investAmountSum,  
    CAST(IFNULL(i.`totalCurrentInvest`,0)/10000 AS DECIMAL(10,4)) currentAmountSum,
    CAST(IFNULL(i.`totalRegularInvest`,0)/10000 AS DECIMAL(10,4)) regularAmountSum,
    CAST(IFNULL(i.`totalFinanceInvest`,0)/10000 AS DECIMAL(10,4)) financierAmountSum,
    DATE(c.`createTime`) registerTime,
    a.`channelname` channelname, 
    ce.`realname` channelEmpName,
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
    a.`channelPlatform` channelPlatform,
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
     a.`channelMode` channelMode,
     (CASE a.`channelMode`
    WHEN '0' THEN '市场渠道'
    WHEN '1' THEN '理财师渠道'
    ELSE ''
      END) channelModeDesc
FROM partner.`t_channel_access` a,partner.`t_channel_emp` ce,partner.`t_channel_user` c
JOIN partner.`t_channel_user_invest_account` i ON i.`userId`=c.`userId`
WHERE IF(a.`channelMode`=0,c.`bindingType`=1,c.`bindingType`=4) AND c.`channelId`=a.`channelId` 
    AND i.`firstInvestTime` BETWEEN '{startTime}' AND '{endTime}' 
    #渠道名称
    AND IF('{channelname}'='', 1=1, a.`channelname` LIKE '%{channelname}%')
    #渠道所属平台
    AND IF('{channelPlatform}'='',1=1, a.`channelPlatform` LIKE '%{channelPlatform}%')
    AND IF('{channelUserName}'='',1=1,ce.`realname`='{channelUserName}') 
    #渠道种类
    AND IF('{channelMode}'='',a.`channelMode`=0, a.`channelMode` = '{channelMode}')
GROUP BY c.`userId` ORDER BY i.`firstInvestTime` DESC, i.`id` DESC LIMIT {rows}) tt;