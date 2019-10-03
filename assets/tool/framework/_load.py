# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-19 14:22:56
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-28 18:34:16
import wx;
import os,sys,time;
import shutil;
# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
# 添加搜索路径
if CURRENT_PATH not in sys.path:
	sys.path.append(CURRENT_PATH);

# 加载core模块
corePath = os.path.join(CURRENT_PATH, "core");
if corePath not in sys.path:
	sys.path.append(corePath);
try:
	import _Global as _G;
	from behaviorCore.BaseBehavior import BaseBehavior;
	from behaviorCore.BehaviorManager import BehaviorManager;
	from eventDispatchCore.EventDispatcher import EventDispatcher;
	from eventDispatchCore.EventId import EVENT_ID;
	from logCore.Logger import Logger;
	from cacheCore.CacheManager import CacheManager;
except Exception as e:
	raise e;
finally:
	sys.path.remove(corePath);

from config import GameConfig;

class Loader(object):
	def __init__(self, mainPath, projectPath):
		super(Loader, self).__init__();
		self._className_ = Loader.__name__;
		self.__mainPath = mainPath.replace("\\", "/");
		self.__projectPath = projectPath.replace("\\", "/");
		_G.initGlobal_GTo_Global(); # 初始化全局变量
		pass;

	def lockGlobal(self):
		_G.lockGlobal_GTo_Global(); # 锁定全局变量

	def loadGlobalInfo(self):
		self.loadUniqueIdFunc(); # 加载唯一Id的全局函数
		self.loadPaths(); # 加载全局路径名变量
		self.loadObjects(); # 加载全局对象变量
		self.loadConfigs(); # 加载全局配置变量
		self.loadResources(); # 加载全局资源变量
		self.loadGClass(); # 加载全局类变量
		pass;

	# 加载唯一Id的全局函数
	def loadUniqueIdFunc(self):
		global uniqueId;
		uniqueId = 0;
		def getUniqueId():
			global uniqueId;
			uniqueId += 1;
			return uniqueId;
		_G.setGlobalVarTo_Global("getUniqueId", getUniqueId);

	# 加载全局路径名变量
	def loadPaths(self):
		_G.setGlobalVarTo_Global("g_ProjectPath", self.__projectPath + "/");
		_G.setGlobalVarTo_Global("g_DataPath", self.__projectPath + "/data/");
		if not os.path.exists(_G._GG("g_DataPath")):
			os.makedirs(_G._GG("g_DataPath")); # 若工程数据文件不存在，则需创建该目录
		_G.setGlobalVarTo_Global("g_AssetsPath", self.__mainPath + "/");
		_G.setGlobalVarTo_Global("g_FrameworkPath", self.__mainPath + "/framework/");
		pass;

	# 加载全局对象变量
	def loadObjects(self):
		_G.setGlobalVarTo_Global("BaseBehavior", BaseBehavior); # 设置组件基础类变量（未实例化）
		_G.setGlobalVarTo_Global("BehaviorManager", BehaviorManager()); # 设置组件管理器的全局变量
		_G.setGlobalVarTo_Global("EventDispatcher", EventDispatcher()); # 设置事件分发器的全局变量
		_G.setGlobalVarTo_Global("EVENT_ID", EVENT_ID); # 设置事件枚举Id的全局变量
		_G.setGlobalVarTo_Global("CacheManager", CacheManager()); # 设置缓存管理器的全局变量
		pass;

	# 加载全局配置变量
	def loadConfigs(self):
		print("Loading game configs......");
		_G.setGlobalVarTo_Global("GameConfig", GameConfig()); # 设置配置的全局变量
		print("Loaded game configs!");
		pass;

	# 加载全局资源变量
	def loadResources(self):
		print("Loading game resources......");
		print("Loaded game resources!");
		pass;

	def loadGClass(self):
		self.loadLogger(); # 加载日志类变量
		pass;

	def loadLogger(self):
		cliConf = _G._GG("GameConfig").Config(); # 服务配置
		path = cliConf.Get("log", "path", "").replace("\\", "/");
		name = cliConf.Get("log", "name", "pytoolsip-tool");
		curTimeStr = time.strftime("%Y_%m_%d", time.localtime());
		logger = Logger("Common", isLogFile = True, logFileName = os.path.join(self.__projectPath, path, name+("_%s.log"%curTimeStr)),
			maxBytes = int(cliConf.Get("log", "maxBytes")), backupCount = int(cliConf.Get("log", "backupCount")));
		_G.setGlobalVarTo_Global("Log", logger); # 设置日志类的全局变量
		return logger;

	# 校验默认数据
	def verifyDefaultData(self):
		_GG = _G._GG;
		# 校验缓存文件夹
		if not os.path.exists(_GG("g_DataPath")+"cache"):
			os.makedirs(_GG("g_DataPath")+"cache");