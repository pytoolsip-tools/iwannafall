# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-01 10:56:10
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-29 17:34:37

from enum import Enum, unique;

# 自增的事件Id函数
global CUR_EVENT_ID;
CUR_EVENT_ID = -1;
def getNewEventId():
	global CUR_EVENT_ID;
	CUR_EVENT_ID += 1;
	return CUR_EVENT_ID;

# 枚举事件Id
@unique
class EVENT_ID(Enum):
	# 获取新的事件ID【供具体工具创建新的事件ID】
	@staticmethod
	def getNewId():
		return getNewEventId();

	K_ESC = getNewEventId(); # ESC按键事件

	K_SPACE = getNewEventId(); # 空格按键事件
	
	K_LEFT = getNewEventId(); # 左按键事件

	K_UP = getNewEventId(); # 上按键事件

	K_RIGHT = getNewEventId(); # 右按键事件
	
	K_DOWN = getNewEventId(); # 下按键事件

	JOYAXISMOTION = getNewEventId(); # 手柄摇杆事件

	JOYBALLMOTION = getNewEventId(); # 手柄追踪球事件

	JOYBUTTONDOWN = getNewEventId(); # 手柄按下按钮事件

	JOYBUTTONUP = getNewEventId(); # 手柄松开按钮事件

	JOYHATMOTION = getNewEventId(); # 手柄键帽事件