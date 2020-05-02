#渠道充值报表汇总                                                                                                                                                                                           
      
SELECT 
    CONCAT(MIN(tt.createTime),'--',MAX(tt.createTime)) createTime, 
    NULL channelname,
    CAST(SUM(tt.registerNum) AS SIGNED) registerNum,
    CAST(SUM(tt.rechargeNum) AS SIGNED) rechargeNum,
    CONCAT(
        (CAST((SUM(tt.rechargeNum) / SUM(tt.registerNum)) * 100 AS DECIMAL(10, 2))),'%') conversionsRates,
    SUM(tt.rechargeAmount) rechargeAmount,
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
    DATE(c.`createTime`) createTime,                                                                                                                                                                                           
    a.`channelname` channelname,                                                                                                                                                                                           
    COUNT(DISTINCT(c.`userId`)) registerNum,                                                                                                                                                                                         
    COUNT(DISTINCT(cr.userId)) rechargeNum,                                                                                                                                                                                     
    CONCAT(
        (CAST((COUNT(DISTINCT(cr.userId)) / COUNT(DISTINCT(c.userId))) * 100 AS DECIMAL(10, 2))),'%')  conversionsRates,  
    (CASE 
        WHEN RIGHT(CAST((SUM(IFNULL(cr.`day1RechargeAmount`, 0)) / 10000) AS DECIMAL(10, 4)), 4) = '0000'  THEN CAST((SUM(IFNULL(cr.`day1RechargeAmount`, 0)) / 10000) AS DECIMAL(10, 1))
        WHEN RIGHT(CAST((SUM(IFNULL(cr.`day1RechargeAmount`, 0)) / 10000) AS DECIMAL(10, 4)), 3) = '000'  THEN CAST((SUM(IFNULL(cr.`day1RechargeAmount`, 0)) / 10000) AS DECIMAL(10, 1))
        WHEN RIGHT(CAST((SUM(IFNULL(cr.`day1RechargeAmount`, 0)) / 10000) AS DECIMAL(10, 4)), 2) = '00'  THEN CAST((SUM(IFNULL(cr.`day1RechargeAmount`, 0)) / 10000) AS DECIMAL(10, 2))
        WHEN RIGHT(CAST((SUM(IFNULL(cr.`day1RechargeAmount`, 0)) / 10000) AS DECIMAL(10, 4)), 1) = '0'  THEN CAST((SUM(IFNULL(cr.`day1RechargeAmount`, 0)) / 10000) AS DECIMAL(10, 3))
        ELSE CAST((SUM(IFNULL(cr.`day1RechargeAmount`, 0)) / 10000) AS DECIMAL(10, 4))
    END ) rechargeAmount,  
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
FROM partner.`t_channel_user_recharge_account` cr 
RIGHT JOIN partner.`t_channel_user` AS c 
ON c.`userId`=cr.`userId` AND DATE(c.`createTime`)=cr.`firstRechargeTime`
JOIN partner.t_channel_access a 
ON a.`channelId`=c.`channelId` AND IF(a.`channelMode`=0,c.`bindingType`=1,c.`bindingType`=4)                                                                                                                      
WHERE                                                                                                                                                                                                                         
    #注册日期                                                                                                                                                                                                                 
    DATE(c.`createTime`) BETWEEN '{startTime}' AND '{endTime}'
    #渠道名称                                                                                                                                                                                                                 
    AND IF('{channelname}'='',1=1,a.`channelname` LIKE '%{channelname}%')  
    #渠道种类
    AND IF('{channelMode}'='',a.`channelMode`=0,a.`channelMode`='{channelMode}')
    #渠道所属功能组                                                                                                                                                                                                           
    AND IF('{channelgroup}'='',1=1,a.`channelGroup`='{channelgroup}')                                                                                                                                                                                                                                                                                                                      
GROUP BY DATE(c.`createTime`),a.`channelId` 
ORDER BY DATE(c.`createTime`) DESC, a.`channelname` 
LIMIT {rows}) AS tt; 
