# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-02-24 05:57:41
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-09 16:40:47
import os;
import json;

try:
	import ConfigParser;
except Exception as e:
	import configparser as ConfigParser;

from _Global import _GG;
from function.base import *;

def GetConfigKeyMap():
	return {
		"Config" : _GG("g_FrameworkPath") + "config/ini/config.ini",
		"PjConfig" : _GG("g_FrameworkPath") + "config/ini/config.json",
	};

class Config(object):
	"""docstring for Config"""
	def __init__(self, pathCfg):
		super(Config, self).__init__();
		self.loadPath(pathCfg);
	
	def loadPath(self, pathCfg):
		self.__initPath__(pathCfg);
		self.__initConfig__();
	
	def __initPath__(self, pathCfg):
		self.__path = "";
		if isinstance(pathCfg, list):
			for path in pathCfg:
				if os.path.exists(path):
					self.__path = path;
					return;
		else:
			self.__path = pathCfg;

	def __initConfig__(self):
		self.__config = ConfigParser.RawConfigParser();
		self.__config.read(self.__path);

	def Set(self, section, option, value):
		if not self.__config.has_section(section):
			self.__config.add_section(section);
		self.__config.set(section, option, value);
		self.__config.write(open(self.__path, "w"), "w");

	def Get(self, section, option, defaultValue = None):
		if self.__config.has_option(section, option):
			return self.__config.get(section, option);
		return defaultValue;


class PjConfig(object):
	"""docstring for PjConfig"""
	def __init__(self, pathCfg):
		super(PjConfig, self).__init__();
		self.loadPath(pathCfg);
	
	def loadPath(self, pathCfg):
		self.__initPath__(pathCfg);
		self.__initConfig__();
	
	def __initPath__(self, pathCfg):
		self.__path = "";
		if isinstance(pathCfg, list):
			for path in pathCfg:
				if os.path.exists(path):
					self.__path = path;
					return;
		else:
			self.__path = pathCfg;

	def __initConfig__(self):
		self.__config = {};
		if os.path.exists(self.__path):
			with open(self.__path, "r") as f:
				self.__config = json.loads(f.read());

	def Get(self, key, defaultVal = None):
		if isinstance(key, list):
			cfg = self.__config;
			for k in key:
				if not isinstance(cfg, dict) or k not in cfg:
					return defaultVal;
				cfg = cfg[k];
			return cfg;
		return self.__config.get(key, defaultVal);


class GameConfig(object):
	"""docstring for GameConfig"""
	def __init__(self,):
		super(GameConfig, self).__init__();
		# 初始化配置对象
		confKeyMap = GetConfigKeyMap();
		self.__config = Config(confKeyMap["Config"]);
		self.__pjConfig = PjConfig(confKeyMap["PjConfig"]);
		pass;

	def Config(self):
		return self.__config;

	def PjConfig(self):
		return self.__pjConfig;