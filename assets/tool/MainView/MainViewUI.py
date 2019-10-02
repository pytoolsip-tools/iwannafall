# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-08 21:02:23
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:46:37
import os, re;
import wx;

from _Global import _GG;
from function.base import *;

class MainViewUI(wx.ScrolledWindow):
	"""docstring for MainViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(MainViewUI, self).__init__(parent, id, size = self.__params["size"]);
		self._className_ = MainViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.bindEvents(); # 绑定事件
		self.SetBackgroundColour(self.__params["bgColour"]);
		# 初始化滚动条参数
		self.SetScrollbars(1, 1, *self.__params["size"]);

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unbindEvents();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : _GG("WindowObject").GetToolWinSize(),
			"style" : wx.BORDER_THEME,
			"bgColour" : wx.Colour(255,255,255),
			"title" : "I WANNA FALL",
			"subTitle" : "【吾欲坠】",
			"extSubTitle" : "- 自制 I Wanna 系列游戏 第一弹 -",
			"btnLabel" : "启动游戏",
			"description" : {
				"title" : "游戏简介",
				"content" : """
  I wanna系列游戏起源于《I wanna be the guy》这款游戏，通过不同制作者的努力，逐渐发展成拥有数千款游戏的系列。
  而我制作的这款游戏，基于Pygame模块开发而成，操作上支持键盘及手柄。
  游戏的故事背景是，主角由从穹顶而来，却被云层阻挡，而无法直落地面。所以，为了穿越云层，主角开始了穿越重重障碍，一往而下的冒险之旅。
""",
			},
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def bindEvents(self):
		_GG("WindowObject").BindEventToToolWinSize(self, self.onToolWinSize);

	def unbindEvents(self):
		_GG("WindowObject").UnbindEventToToolWinSize(self);

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.resetScrollbars(); # 重置滚动条

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		self.createTitle();
		self.createGameCtrl();
		self.createDescription();
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__title, flag = wx.ALIGN_CENTER);
		box.Add(self.__gameCtrl, flag = wx.ALIGN_CENTER);
		box.Add(self.__description, flag = wx.ALIGN_CENTER);
		self.SetSizer(box);
		totalHeight = self.__title.GetSize().y + self.__gameCtrl.GetSize().y + self.__description.GetSize().y;
		if self.GetSize().y < totalHeight:
			self.Fit();
		pass;

	def resetScrollbars(self):
		self.SetScrollbars(1, 1, self.GetSizer().GetSize().x, self.GetSizer().GetSize().y);

	def onToolWinSize(self, sizeInfo, event = None):
		self.SetSize(self.GetSize() + sizeInfo["preDiff"]);
		self.Refresh();
		self.Layout();

	def updateView(self, data):
		pass;

	def createTitle(self):
		self.__title = wx.Panel(self, size = (self.GetSize().x, -1), style = wx.BORDER_THEME)
		mainTitle = wx.StaticText(self.__title, label = self.__params["title"]);
		mainTitle.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline=True));
		subTitle = wx.StaticText(self.__title, label = self.__params["subTitle"]);
		subTitle.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		extSubTitle = wx.StaticText(self.__title, label = self.__params["extSubTitle"]);
		extSubTitle.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(wx.Panel(self.__title), flag = wx.TOP, border = 20);
		box.Add(mainTitle, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(subTitle, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(extSubTitle, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(wx.Panel(self.__title), flag = wx.BOTTOM, border = 20);
		self.__title.SetSizer(box);

	def createGameCtrl(self):
		self.__gameCtrl = wx.Panel(self, size = (self.GetSize().x, -1), style = wx.BORDER_THEME);
		runGame = wx.Button(self.__gameCtrl, label = self.__params["btnLabel"], size = (200, 60));
		# runGame = wx.BitmapButton(self.__gameCtrl, bitmap = self.__params["btnImg"]);
		runGame.Bind(wx.EVT_BUTTON, self.runGame);
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(wx.Panel(self.__gameCtrl), flag = wx.TOP, border = 20);
		box.Add(runGame, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(wx.Panel(self.__gameCtrl), flag = wx.BOTTOM, border = 20);
		self.__gameCtrl.SetSizer(box);

	# 获取对应名称的脚本
	def getFile(self, dirPath, name):
		for fn in os.listdir(dirPath):
			fPath = os.path.join(dirPath, fn);
			if os.path.isfile(fPath) and re.search(f"{name}\.?.*\.pyc", fn):
				return fn;
		return f"{name}.py";

	def runGame(self, event = None):
		pyExe = os.path.abspath(os.path.join(_GG("g_PythonPath"), "python.exe"));
		toolPath = GetPathByRelativePath("../", self._curPath);
		mainFileName = self.getFile(toolPath, "main");
		# 更新run.bat文件
		runFilePath = VerifyPath(os.path.join(toolPath, "run.bat"));
		if os.path.exists(runFilePath):
			content = "";
			with open(runFilePath, "r", encoding = "utf-8") as f:
				for line in f.readlines():
					if re.search("set pyexe.*=.*", line):
						line = "set pyexe=" + VerifyPath(pyExe) + "\n";
					elif re.search("set pjfile.*=.*", line):
						line = "set pjfile=" + VerifyPath(toolPath) + "\n";
					elif re.search("set mainfile.*=.*", line):
						line = "set mainfile=" + VerifyPath(mainFileName) + "\n";
					content += line;
			with open(runFilePath, "w", encoding = "utf-8") as f:
				f.write(content);
		# 运行run.bat文件
		os.system(" ".join(["start", os.path.abspath(runFilePath)]));
		pass;

	def createDescription(self):
		params = self.__params["description"];
		self.__description = wx.Panel(self, size = (self.GetSize().x, -1), style = wx.BORDER_THEME);
		title = wx.StaticText(self.__description, label = params["title"]);
		title.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline=True));
		textCtrl = wx.TextCtrl(self.__description, value = params["content"], size = (self.GetSize().x, 300), style = wx.TE_MULTILINE|wx.TE_READONLY);
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(wx.Panel(self.__description), flag = wx.TOP, border = 20);
		box.Add(title, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(textCtrl, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(wx.Panel(self.__description), flag = wx.BOTTOM, border = 20);
		self.__description.SetSizer(box);