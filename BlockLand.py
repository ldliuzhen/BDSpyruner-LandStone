import mc
import os
import json
print('[破晓] 领地石插件加载完毕! ————by 那个男人')

def onEnable():
	global ConfigData
	global LandFile
	global LandData
	global LandDataNotEmpty
	global RecordFile
	global RecordData
	global RecordDataNotEmpty
	global LandShareFile
	global LandShareData
	global LandShareDataNotEmpty
	global shareModeCase        #共享状态开关0关闭，1添加共享，2删除共享
	global sendSharePlayerInfo
	if os.path.exists(os.getcwd()+"/plugins/BlockLand/Config.json"):
		ConfigFile = open(os.getcwd()+"/plugins/BlockLand/Config.json")
		ConfigData = json.load(ConfigFile)
		LandFile = open(os.getcwd()+"/plugins/BlockLand/Land.json",mode='r+',encoding='utf-8')
		RecordFile = open(os.getcwd()+"/plugins/BlockLand/Record.json",mode='r+',encoding='utf-8')
		LandShareFile = open(os.getcwd()+"/plugins/BlockLand/LandShare.json",mode='r+',encoding='utf-8')
		if os.path.getsize(os.getcwd()+"/plugins/BlockLand/Land.json") != 0:       #判断文件是否为空
			LandData = json.load(LandFile)          #注意只能有一个总字典，不然会报错,总字典：json文件最大的那个{}
			LandDataNotEmpty = True
			LandFile.close()
		else:
			LandDataNotEmpty = False
		if os.path.getsize(os.getcwd()+"/plugins/BlockLand/Record.json") != 0:
			RecordData = json.load(RecordFile)
			RecordDataNotEmpty = True
		else:
			RecordDataNotEmpty = False
		if  os.path.getsize(os.getcwd()+"/plugins/BlockLand/LandShare.json") != 0:
			LandShareData = json.load(LandShareFile)
			LandShareDataNotEmpty = True
			LandShareFile.close()
		else:
			LandShareDataNotEmpty = False
	else:
		os.mkdir(os.getcwd()+'/plugins/BlockLand')
		#创建配置文件
		DefaultData = {'领地石ID':57,'领地石保护半径':20,'主世界是否生效':True,'地狱是否生效':False,'末地是否生效':False,'是否开启Z轴领地':False,'OP可操作':True,'OP操作日志是否开启':False}   #True和False必须开头大写，小写会报错，如要保存字符串则加上''
		ConfigData = json.dumps(DefaultData,ensure_ascii=False,indent=2)          #把ascii编码关掉，不然会以json字符储存，indent表示缩进长度
		ConfigFile = open(os.getcwd()+"/plugins/BlockLand/Config.json",mode='w+')        #w+可以让未存在的文件创建，但是也会清空文件内容，慎用
		ConfigFile.write(ConfigData)
		ConfigFile.close()
		ConfigFile = open(os.getcwd()+"/plugins/BlockLand/Config.json")
		ConfigData = json.load(ConfigFile)
		#创建日志文件
		LandFile = open(os.getcwd()+"/plugins/BlockLand/Land.json",mode='w+')
		RecordFile = open(os.getcwd()+"/plugins/BlockLand/Record.json",mode='w+')
		LandDataNotEmpty = False
		RecordDataNotEmpty = False
		#创建领地共享文件
		LandShareFile = open(os.getcwd()+"/plugins/BlockLand/LandShare.json",mode='w+')
		LandShareDataNotEmpty = False
	shareModeCase = {}
	sendSharePlayerInfo = {}
	return True

onEnable()
#====================================控制台指令事件============================================================================================

def onPlayerCMD(event):
	global sendSharePlayerInfo
	global shareModeCase
	getCMD = event['cmd']
	if len(getCMD) < 50:         #判断字符串长度,防止恶意刷长指令
		if getCMD == '/领地石':
			getTriggerPlayer = event['player']
			massage = '§2领地石帮助列表:\n/领地石 §f添加共享 共享玩家名称\n§2/领地石 §f删除共享 共享玩家名称'
			getTriggerPlayer.sendTextPacket(massage,6)
			return False         #拦截指令，不然会出现未知指令
		if '' in getCMD:
			getCMDArray = getCMD.split(' ')        #分割字符串，默认空格
		if getCMDArray[0] == '/领地石':
			getTriggerPlayer = event['player']
			getPlayerName = getTriggerPlayer.name
			if getCMDArray[0] == '/领地石'and getCMDArray[1] is None:
				massage = '§2领地石帮助列表:\n/领地石 §f添加共享 共享玩家名称\n§2/领地石 §f删除共享 共享玩家名称'
				getTriggerPlayer.sendTextPacket(massage,6)
				return False
			if getCMDArray[1] != '帮助' and getCMDArray[1] != '添加共享' and getCMDArray[1] != '删除共享':
				massage = '§e[领地石]§f错误!请输入正确的指令,如需查看帮助请输入§a/领地石 帮助'
				getTriggerPlayer.sendTextPacket(massage,6)
				return False
			if getCMDArray[1] == '帮助':
				massage = '§2领地石帮助列表:\n/领地石 §f添加共享 共享玩家名称\n§2/领地石 §f删除共享 共享玩家名称'
				getTriggerPlayer.sendTextPacket(massage,6)
				return False
			if getCMDArray[1] == '添加共享':
				if getCMDArray[2] is None:
					massage = '§4[领地石]错误,未定义对象!'
					getTriggerPlayer.sendTextPacket(massage,6)
					return False
				sendSharePlayerInfo[getPlayerName] = getCMDArray[2]          #向传递字典变量中添加需要传递的玩家信息
				massage = '§e[领地石]§f共享开始,请在需要共享的领地上放置任意方块!'
				getTriggerPlayer.sendTextPacket(massage,6)
				shareModeCase[getPlayerName] = 1              #新增触发玩家状态字典
				return False
			if getCMDArray[1] == '删除共享':
				if getCMDArray[2] is None:
					massage = '§4[领地石]错误,未定义对象!'
					getTriggerPlayer.sendTextPacket(massage,6)
					return False
				sendSharePlayerInfo[getPlayerName] = getCMDArray[2]
				massage = '§e[领地石]§f删除开始,请在需要解除共享的领地上放置任意方块!'
				getTriggerPlayer.sendTextPacket(massage,6)
				shareModeCase[getPlayerName] = 2
				return False
	return True

#====================================文件重置与写入事件===================================================================================================
def LandFileReset():
	global LandFile
	LandFile = open(os.getcwd()+"/plugins/BlockLand/Land.json",mode='w+',encoding='utf-8')          

def LandShareFileReset():
	global LandShareFile
	LandShareFile = open(os.getcwd()+"/plugins/BlockLand/LandShare.json",mode='w+',encoding='utf-8')       #先清空再写入
	LandShareFile.write(LandShareData)
	LandShareFile.close()

#====================================领地石功能判断函数===============================================================================================
def BlockWorldJudgment(level):
	if level == 0 and ConfigData['主世界是否生效'] == True:
		return True 
	if level == 1 and ConfigData['地狱是否生效'] == True:
		return True
	if level == 2 and ConfigData['末地是否生效'] == True:
		return True
	return False

def BlockEventJudgment(playerName,blockKey,position,playerInfo):         #本函数返回真则表示，事件方块不在领地范围内或属于领地主人自身
	if blockKey in LandData:     #检查传过来的键值参数是否在LandData字典变量中
		for Key,Value in LandData.items():
			if Key == blockKey:    #对比破坏领地石的玩家是否为领地石的主人
				if playerName == Value['所属玩家']:
					return True
				else:
					return Value['所属玩家']
	else:
		if ConfigData['是否开启Z轴领地'] == True:
			BlockX = position[0]
			BlockY = position[1]            
			BlockZ = position[2]
			for Key,Value in LandData.items():       #遍历LandData中的所有键与值
				if int(Value['X1']) < BlockX <int(Value['X2']) and int(Value['Y1']) < BlockY < int(Value['Y2']) and int(Value['Z1']) < BlockZ < int(Value['Z2']):
					if playerName == Value['所属玩家']:#注意在字典dict中Value[5]这种用法是错误的（键与值），这种用法是列表list的用法（数组与指针）
						ShareInfoAddJudgment(playerName,playerInfo,Key,Value)
						ShareInfoDelJudgment(playerName,playerInfo,Key,Value)
						return True
					else:
						return LandBelongPlayer
		else:
			BlockX = position[0]
			BlockZ = position[2]		#我的世界高度信息在Y轴里
			for Key,Value in LandData.items():
				if int(Value['X1']) < BlockX < int(Value['X2']) and int(Value['Z1']) < BlockZ < int(Value['Z2']):
					if playerName == Value['所属玩家']:
						ShareInfoAddJudgment(playerName,playerInfo,Key,Value)
						ShareInfoDelJudgment(playerName,playerInfo,Key,Value)
						return True
					else:
						if Value['是否共享'] == True:
							if playerName in LandShareData[Key]:
								return True
						LandBelongPlayer = Value['所属玩家']
						return LandBelongPlayer			
	return True

def ShareInfoAddJudgment(playerName,playerInfo,Key,Value):                  #添加共享信息函数
	global shareModeCase
	global LandShareData
	global LandShareDataNotEmpty
	if playerName in shareModeCase:         #检查该玩家的分享状态指针
		if shareModeCase[playerName] == 1 and sendSharePlayerInfo[playerName] is not None:
			if LandShareDataNotEmpty == False:
				Temp = {sendSharePlayerInfo[playerName]:True}
				LandShareData = {Key:Temp}
				LandShareData = json.dumps(LandShareData,ensure_ascii=False,indent=2)
				LandShareFileReset()
				LandShareData = json.loads(LandShareData)   #从内存加载
				LandShareDataNotEmpty = True
				Temp = LandData[Key]
				Temp['是否共享'] = True
				LandData[Key] = Temp
				writeDataToJson = json.dumps(LandData,ensure_ascii=False,indent=2)
				LandFileReset()
				LandFile.write(writeDataToJson)
				LandFile.close()
				massage = '§e[领地石]§f共享成功!'
				playerInfo.sendTextPacket(massage,6)
				shareModeCase[playerName] = 0
				return
			else:
				if Key in LandShareData:
					Temp = LandShareData[Key]  
					Temp2 = sendSharePlayerInfo[playerName]
					Temp[Temp2] = True    #往二级字典中添加共享者信息
					LandShareData[Key] = Temp
				else:
					LandShareData[Key] = {sendSharePlayerInfo[playerName]:True}
					Temp = LandData[Key]
					Temp['是否共享'] = True
					LandData[Key] = Temp
					writeDataToJson = json.dumps(LandData,ensure_ascii=False,indent=2)
					LandFileReset()
					LandFile.write(writeDataToJson)
					LandFile.close()					
				LandShareData = json.dumps(LandShareData,ensure_ascii=False,indent=2)
				LandShareFileReset()
				LandShareData = json.loads(LandShareData)
				massage = '§e[领地石]§f共享成功!'
				playerInfo.sendTextPacket(massage,6)
				shareModeCase[playerName] = 0
				return
		else:
			shareModeCase[playerName] == 0

def ShareInfoDelJudgment(playerName,playerInfo,Key,Value):          #删除共享信息函数
	global shareModeCase
	global LandShareData
	global LandShareDataNotEmpty
	if playerName in shareModeCase:         #检查该玩家的分享状态指针
		if shareModeCase[playerName] == 2 and sendSharePlayerInfo[playerName] is not None:
			if LandShareDataNotEmpty == False:
				massage = '§e[领地石]§4错误删除!没有信息！'
				playerInfo.sendTextPacket(massage,6)
				shareModeCase[playerName] = 0
				return False
			else:
				if Key in LandShareData:
					if sendSharePlayerInfo[playerName] in LandShareData[Key]:
						Temp = LandShareData[Key]
						Temp2 = sendSharePlayerInfo[playerName]
						del Temp[Temp2]                #删除子字典中的值
						LandShareData[Key] = Temp
						if LandShareData[Key] is None:           #如果这个共享点位Key已经没有任何值，则删除
							del LandShareData[Key]
						LandShareData = json.dumps(LandShareData,ensure_ascii=False,indent=2)
						LandShareFileReset()
						LandShareData = json.loads(LandShareData)						
						massage = '§e[领地石]§a此领地与玩家'+'§f'+sendSharePlayerInfo[playerName]+'§a解除共享成功！'
						playerInfo.sendTextPacket(massage,6)
						shareModeCase[playerName] = 0
						return True
					else:
						massage = '§e[领地石]§4错误删除!这个领地没有这个玩家的信息！'
						playerInfo.sendTextPacket(massage,6)
						shareModeCase[playerName] = 0
						return False												
				else:
					massage = '§e[领地石]§4错误删除!这个领地没有任何共享玩家！'
					playerInfo.sendTextPacket(massage,6)
					shareModeCase[playerName] = 0
					return False					

#===================================领地石功能函数==================================================================================================
			
def onBlockPlace(event):                        #函数中的(event)就是监听参数setListener传来的，比如方块破坏事件就会传递成$this->$event->onBlockPlace(PHP表示)事件,event相当于mc.onPlaceBlock()   AP
	global LandDataNotEmpty						#py修改全局变量必须在函数里再次申明
	global RecordDataNotEmpty
	global LandFile
	global LandData
	global RecordData
	getTriggerPlayer = event["player"]			#从放置事件中获得触发玩家，event["player"]属于API
	getBlockName = event["blockname"]			#从放置事件中获得触发方块名称
	getBlockID =event["blockid"]
	getBlockPosition = event["position"]
	BlockX1 = getBlockPosition[0] - int(ConfigData['领地石保护半径'])
	BlockX2 = getBlockPosition[0] + int(ConfigData['领地石保护半径'])
	BlockY1 = getBlockPosition[1] - int(ConfigData['领地石保护半径'])
	BlockY2 = getBlockPosition[1] + int(ConfigData['领地石保护半径'])
	BlockZ1 = getBlockPosition[2] - int(ConfigData['领地石保护半径'])
	BlockZ2 = getBlockPosition[2] + int(ConfigData['领地石保护半径'])
	getWorld = getTriggerPlayer.did            #获取玩家所在的世界,由于mc模块中本身未对EntityObject()这个类进行定义，所以不能使用mc.EntityObject()
	getPlayerName = getTriggerPlayer.name        #查询玩家的名称
	if BlockWorldJudgment(getWorld) == True:
		BlockKey = str(getBlockPosition[0])+'.'+str(getBlockPosition[1])+'.'+str(getBlockPosition[2])#整数型转字符串
		if getWorld == 0:
			levelName = 'world'
		if getWorld == 1:
			levelName = 'nether'
		if getWorld == 2:
			levelName = 'ender'
		BlockInfo = {'X1':BlockX1,'X2':BlockX2,'Y1':BlockY1,'Y2':BlockY2,'Z1':BlockZ1,'Z2':BlockZ2,'所属世界':levelName,'所属玩家':getPlayerName,'是否共享':False}
		"""
		写入方块信息进入变量
		BlockKey:BlockX1   BlockKey为键：BlockX1为值
		一个json文件只能有一个总字典，所以得用多重字典的方式新增信息
		"""
		if LandDataNotEmpty == False:
			if getBlockID == ConfigData['领地石ID']:
				writeData = {BlockKey:BlockInfo}       #一个json文件只能有一个总目录Key
				writeDataToJson = json.dumps(writeData,ensure_ascii=False,indent=2)
				LandFile.write(writeDataToJson)
				LandFile.close()                 #由于Land文件最开始没有内容，所以第一次写入后先关闭文件再加载，不然json.load会报错
				LandData = writeData        
				LandDataNotEmpty = True
				massage = '§e领地石已上线,领地保护系统启动!'
				getTriggerPlayer.sendTextPacket(massage,6)       #1为聊天文本			
		else:
			FunctionReturnValue = BlockEventJudgment(getPlayerName,BlockKey,getBlockPosition,getTriggerPlayer)
			if FunctionReturnValue == True or getTriggerPlayer.perm == 1:       #检查返回值和是否为OP
				if getBlockID == ConfigData['领地石ID']:				
					LandData[BlockKey] = BlockInfo     #直接在变量中声明新增的键值即可,本段作用，往LandData变量中新增刚刚放下的方块信息          
					writeDataToJson = json.dumps(LandData,ensure_ascii=False,indent=2)
					LandFileReset()
					LandFile.write(writeDataToJson)
					LandFile.close()
					massage = '§e[领地石]§a领地已上线,保护系统启动!'
					getTriggerPlayer.sendTextPacket(massage,6)
			else:
				massage = '§e[领地石]§4此处为'+FunctionReturnValue+'的领地,不可放置!'
				getTriggerPlayer.sendTextPacket(massage,6)
				return False      #拦截本事件
		#LandFile.flush()             #刷新文件缓存
	return True

def onBlockBreak(event):                        
	global LandDataNotEmpty						
	global RecordDataNotEmpty
	global LandFile
	global LandData
	global RecordData
	getTriggerPlayer = event["player"]			
	getBlockName = event["blockname"]			
	getBlockID =event["blockid"]
	getBlockPosition = event["position"]
	BlockX1 = getBlockPosition[0] - int(ConfigData['领地石保护半径'])
	BlockX2 = getBlockPosition[0] + int(ConfigData['领地石保护半径'])
	BlockY1 = getBlockPosition[1] - int(ConfigData['领地石保护半径'])
	BlockY2 = getBlockPosition[1] + int(ConfigData['领地石保护半径'])
	BlockZ1 = getBlockPosition[2] - int(ConfigData['领地石保护半径'])
	BlockZ2 = getBlockPosition[2] + int(ConfigData['领地石保护半径'])
	getWorld = getTriggerPlayer.did            
	getPlayerName = getTriggerPlayer.name        
	if BlockWorldJudgment(getWorld) == True:
		BlockKey = str(getBlockPosition[0])+'.'+str(getBlockPosition[1])+'.'+str(getBlockPosition[2])
		if getWorld == 0:
			levelName = 'world'
		if getWorld == 1:
			levelName = 'nether'
		if getWorld == 2:
			levelName = 'ender'
		BlockInfo = {'X1':BlockX1,'X2':BlockX2,'Y1':BlockY1,'Y2':BlockY2,'Z1':BlockZ1,'Z2':BlockZ2,'所属世界':levelName,'所属玩家':getPlayerName,'是否共享':False}
		if LandDataNotEmpty == True: 
			FunctionReturnValue = BlockEventJudgment(getPlayerName,BlockKey,getBlockPosition,getTriggerPlayer)
			if FunctionReturnValue == True or getTriggerPlayer.perm == 1: 
				if getBlockID == ConfigData['领地石ID']:
					del LandData[BlockKey]		#删除LandData字典中的键值		     
					writeDataToJson = json.dumps(LandData,ensure_ascii=False,indent=2)
					LandFileReset()
					LandFile.write(writeDataToJson)
					LandFile.close()
					massage = '§e[领地石]§a领地石已经拆除,保护系统关闭!'
					getTriggerPlayer.sendTextPacket(massage,6)
			else:
				massage = '§e[领地石]§4此处为'+FunctionReturnValue+'的领地,不可破坏!'
				getTriggerPlayer.sendTextPacket(massage,6)
				return False  
	return True

def onChestOpen(event): 
	global RecordData
	getTriggerPlayer = event["player"]	
	getChestPosition = event["position"]
	getWorld = getTriggerPlayer.did            
	getPlayerName = getTriggerPlayer.name        
	if BlockWorldJudgment(getWorld) == True:
		if LandDataNotEmpty == True: 
			BlockKey = str(getChestPosition[0])+'.'+str(getChestPosition[1])+'.'+str(getChestPosition[2])
			FunctionReturnValue = BlockEventJudgment(getPlayerName,BlockKey,getChestPosition,getTriggerPlayer)
			if FunctionReturnValue == True or getTriggerPlayer.perm == 1: 
				return True
			else:
				massage = '§e[领地石]§4此处为'+FunctionReturnValue+'的领地,不可开启这个箱子!'
				getTriggerPlayer.sendTextPacket(massage,6)
				return False  
	return True

def onUseItems(event):         #物品使用事件
	global RecordData
	getTriggerPlayer = event["player"]	
	getItemName = event["itemname"]
	getBlockPosition = event["position"]        #获取被操作的方块位置
	getWorld = getTriggerPlayer.did            
	getPlayerName = getTriggerPlayer.name        
	if BlockWorldJudgment(getWorld) == True:
		if getItemName == 'water_bucket' or getItemName == 'lava_bucket':           #判断桶
			if LandDataNotEmpty == True: 
				BlockKey = str(getBlockPosition[0])+'.'+str(getBlockPosition[1])+'.'+str(getBlockPosition[2])
				FunctionReturnValue = BlockEventJudgment(getPlayerName,BlockKey,getBlockPosition,getTriggerPlayer)
				if FunctionReturnValue == True or getTriggerPlayer.perm == 1: 
					return True
				else:
					massage = '§e[领地石]§4此处为'+FunctionReturnValue+'的领地,不可以使用这个物品!'
					getTriggerPlayer.sendTextPacket(massage,6)
					return False  
	return True

def OnFieldBreak(event):
	global RecordData
	getTriggerPlayer = event["player"]
	getBlockPosition = event["position"]
	getWorld = getTriggerPlayer.did
	getPlayerName = getTriggerPlayer.name
	if BlockWorldJudgment(getWorld) == True:
		if LandDataNotEmpty == True:
			BlockKey = str(getBlockPosition[0])+'.'+str(getBlockPosition[1])+'.'+str(getBlockPosition[2])
			FunctionReturnValue = BlockEventJudgment(getPlayerName,BlockKey,getBlockPosition,getTriggerPlayer)
			if FunctionReturnValue == True or getTriggerPlayer.perm == 1:
				return True
			else:
				massage = '§e[领地石]§4此处为'+FunctionReturnValue+'的领地,不可以破坏耕地!'
				getTriggerPlayer.sendTextPacket(massage,6)
				return False
	return True


#=========================监听事件===================================
mc.setListener('放置方块',onBlockPlace)
mc.setListener('破坏方块',onBlockBreak)
mc.setListener('打开箱子',onChestOpen)
mc.setListener('使用物品',onUseItems)
mc.setListener('输入指令',onPlayerCMD)
mc.setListener('耕地破坏',OnFieldBreak)
mc.setCommandDescription('领地石','打开领地石帮助菜单')
mc.setCommandDescription('领地石 帮助','打开领地石帮助菜单')
mc.setCommandDescription('领地石 添加共享 共享玩家名称','分享一个领地石的共享')
mc.setCommandDescription('领地石 删除共享 共享玩家名称','删除一个领地石的共享')

def Test():
	for Key,Value in LandData.items():
		print(Key)