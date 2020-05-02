#渠道管理

SELECT 
	ca.`authority` authority,
	ca.`channelCode` channelCode,
	ca.`channelDevice` channelDevice,
	(CASE ca.`channelDevice`                                                                                                                                                                                                  
		WHEN '1' THEN 'PC'                                                                                                                                                                                                   
		WHEN '2' THEN 'WAP'                                                                                                                                                                                                  
		WHEN '3' THEN '线下' 
		WHEN '4' THEN 'APP选项'  
		ELSE ''                                                                                                                                                                                               
	END) channelDeviceDesc,
	ca.`channelEmpId` channelEmpId,
	ca.`channelGroup` channelGroup,
	(CASE ca.`channelGroup`        
		WHEN '1' THEN 'SNS推广'
		WHEN '2' THEN '渠道合作'
		WHEN '3' THEN '数字营销'
		WHEN '4' THEN '客户服务'
		WHEN '5'  THEN '移动推广'
		WHEN '6'  THEN '移动运营'
		WHEN '7'  THEN '品牌推广'
		WHEN '8'  THEN '其他'   
		ELSE ''                                                                                                                                                                                                
	END) channelGroupDesc,
	ca.`channelId` channelId,
	ca.`channelindex` channelindex,
	ca.`channelMode` channelMode,
	(CASE ca.`channelMode`
		WHEN '0' THEN '市场渠道'
		WHEN '1' THEN '理财师渠道'
		ELSE ''
	END) channelModeDesc,
	ca.`channelname` channelname,
	ca.`channelPlatform` channelPlatform,
	ca.`channelSupplier` channelSupplier,
	ca.`channelSupplierId` channelSupplierId,
	ca.`channeltype` channeltype,
	(CASE ca.`channeltype`                                                                                                                                                                                                     
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
	ce.`username` channelUseName,
	ca.`createTime` createTime,
	null createTimeStr,
	ca.`creator` creator,
	ca.`dataAuthorityEnable` dataAuthorityEnable,
	null dataAuthorityEnableStr,
	ca.`detail` detail,
	ca.`groundingTime` groundingTime,
	ca.`hasReferee` hasReferee,
	ca.`id` id,
	ca.`modifier` modifier,
	ca.`modifyTime` modifyTime,
	ca.`parentChannelId` parentChannelId,
	ca.`rootChannelId` rootChannelId,
	ca.`state` state,
	ca.`supplierLinkman` supplierLinkman,
	ca.`supplierlinkPhone` supplierlinkPhone
FROM partner.`t_channel_access` ca
LEFT JOIN partner.`t_channel_emp` ce
ON ca.`channelEmpId`=ce.`id`
WHERE IF('{channelindex}'='',1=1,ca.`channelindex`='{channelindex}') 
AND IF('{channelname}'='',1=1,ca.`channelname` LIKE '%{channelname}%') 
AND IF('{username}'='',1=1,ce.`username`='{username}') 
AND IF('{channelMode}'='',1=1,ca.`channelMode`='{channelMode}')
ORDER BY ca.`id` DESC LIMIT {rows};