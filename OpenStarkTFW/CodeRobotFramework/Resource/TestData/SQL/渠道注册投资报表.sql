#渠道注册投资报表   
                                                                                                                                                                                                                            
SELECT                                                                                                                                                                                                                        
    ca.`accountingTime` createTime,                                                                                                                                                                                           
    a.`channelname` channelname, 
    NULL channelId,                                                                                                                                                                                                
    ca.`registerNum` registerNum,                                                                                                                                                                                         
    (CASE {day}
    WHEN '0' THEN IFNULL(ca.`day1InvestNum`, 0)
    WHEN '6' THEN IFNULL(ca.`day7InvestNum`,0)
    WHEN '29' THEN IFNULL(ca.`day30InvestNum`,0)
    WHEN '44' THEN IFNULL(ca.`day45InvestNum`,0)
    WHEN '89' THEN IFNULL(ca.`day90InvestNum`,0)
    END) investorNum, 
    (CASE {day}
    WHEN '0' THEN CONCAT(CAST((ca.`day1InvestNum` / ca.`registerNum` * 100) AS DECIMAL(10, 2)), '%')
    WHEN '6' THEN CONCAT(CAST((ca.`day7InvestNum` / ca.`registerNum` * 100) AS DECIMAL(10, 2)), '%')
    WHEN '29' THEN CONCAT(CAST((ca.`day30InvestNum` / ca.`registerNum` * 100) AS DECIMAL(10, 2)), '%')
    WHEN '44' THEN CONCAT(CAST((ca.`day45InvestNum` / ca.`registerNum` * 100) AS DECIMAL(10, 2)), '%')
    WHEN '89' THEN CONCAT(CAST((ca.`day90InvestNum` / ca.`registerNum` * 100) AS DECIMAL(10, 2)), '%')
    END) conversionsRates,   
    (CASE {day}
    WHEN '0' THEN CAST(SUM(IFNULL((i.`day1CurrentInvest`+i.`day1RegularInvest`),0))/10000 AS DECIMAL(10,4))
    WHEN '6' THEN CAST(SUM(IFNULL((i.`day7CurrentInvest`+i.`day7RegularInvest`),0))/10000 AS DECIMAL(10,4))
    WHEN '29' THEN CAST(SUM(IFNULL((i.`day30CurrentInvest`+i.`day30RegularInvest`),0))/10000 AS DECIMAL(10,4))
    WHEN '44' THEN CAST(SUM(IFNULL((i.`day45CurrentInvest`+i.`day45RegularInvest`),0))/10000 AS DECIMAL(10,4))
    WHEN '89' THEN CAST(SUM(IFNULL((i.`day90CurrentInvest`+i.`day90RegularInvest`),0))/10000 AS DECIMAL(10,4))
    END) investAmount,  
    (CASE {day}
    WHEN '0' THEN CAST(SUM(IFNULL(i.`day1CurrentInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '6' THEN CAST(SUM(IFNULL(i.`day7CurrentInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '29' THEN CAST(SUM(IFNULL(i.`day30CurrentInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '44' THEN CAST(SUM(IFNULL(i.`day45CurrentInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '89' THEN CAST(SUM(IFNULL(i.`day90CurrentInvest`,0))/10000 AS DECIMAL(10,4))
    END) currentAmount,
    (CASE {day}
    WHEN '0' THEN CAST(SUM(IFNULL(i.`day1RegularInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '6' THEN CAST(SUM(IFNULL(i.`day7RegularInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '29' THEN CAST(SUM(IFNULL(i.`day30RegularInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '44' THEN CAST(SUM(IFNULL(i.`day45RegularInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '89' THEN CAST(SUM(IFNULL(i.`day90RegularInvest`,0))/10000 AS DECIMAL(10,4))
    END) regularAmount,
    (CASE {day}
    WHEN '0' THEN CAST(SUM(IFNULL(i.`day1FinanceInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '6' THEN CAST(SUM(IFNULL(i.`day7FinanceInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '29' THEN CAST(SUM(IFNULL(i.`day30FinanceInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '44' THEN CAST(SUM(IFNULL(i.`day45FinanceInvest`,0))/10000 AS DECIMAL(10,4))
    WHEN '89' THEN CAST(SUM(IFNULL(i.`day90FinanceInvest`,0))/10000 AS DECIMAL(10,4))
    END) financierAmount,
    ce.`realname` channelEmpName,
    a.`channeltype` channeltype,
    (CASE a.`channeltype`                                                                                                                                                                                                     
        WHEN '1' THEN 'BD合作类'  #1BD合作类、2垂直媒体类、3品牌类、41效果类-DSP、42效果类-SEM、43效果类-其他、44效果类-信息流、45效果类-自媒体、5资源互换类                                                                  
        WHEN '2' THEN '垂直媒体类'                                                                                                                                                                                            
        WHEN '3' THEN '品牌类'                                                                                                                                                                                                
        WHEN '41' THEN '效果类-DSP'                                                                                                                                                                                           
        WHEN '42' THEN '效果类-SEM'                                                                                                                                                                                           
        WHEN '43' THEN '效果类-其他'                                                                                                                                                                                          
        WHEN '44' THEN '效果类-信息流'                                                                                                                                                                                        
        WHEN '45' THEN '效果类-自媒体'                                                                                                                                                                                        
        WHEN '5' THEN '资源互换类'   
        WHEN '6'  THEN '论坛贴吧类' 
        WHEN '7' THEN '效果类-应用市场'   
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
FROM partner.t_channel_access a, partner.`t_channel_emp` ce, partner.`t_channel_user_account_relationship` c 
RIGHT JOIN partner.`t_channel_account` ca ON c.`channelAccountId`=ca.`id` 
LEFT JOIN partner.`t_channel_user_invest_account` i ON i.`userId` = c.`userId`                                                                                                                 
WHERE    
    a.`channelEmpId`=ce.`id` OR a.`channelId` = ca.`channelId`                                                                                                     
    #注册日期 
    AND ca.`accountingTime` BETWEEN '{startTime}' AND '{endTime}'
    #渠道名称                                                                                                                                                                                                                 
    AND IF('{channelname}'='',1=1,a.`channelname` LIKE '%{channelname}%') 
    AND IF('{channelUseName}'='',1=1,ce.`realname`='{channelUseName}')                                                                                                                                                                                                                                                                 
    #渠道所属平台                                                                                                                                                                                                             
    AND IF('{channelPlatform}'='',1=1,a.`channelPlatform` LIKE '%{channelPlatform}%')                                                                                                   
    #渠道种类
    AND IF('{channelMode}'='',a.`channelMode`=0,a.`channelMode`='{channelMode}')                                                                                                                                                                                                                     
GROUP BY ca.`accountingTime`,a.`channelId` ORDER BY ca.`accountingTime` DESC, a.`channelname` ASC LIMIT {rows};