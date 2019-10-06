import math;
import pygame;

from _Global import _GG;
from function.base import *;

from ui import *;

def onTrigger(view):
	if not hasattr(view, "m_isTriggered") or not view.m_isTriggered:
		view.m_isTriggered = True;
		updateParams = view.params.get("update", {});
		# 显示view
		if "visible" in updateParams:
			view.visible = updateParams["visible"];
		# 移动view
		if "offset" in updateParams:
			offsetX, offsetY = updateParams["offset"];
			view.rect.move_ip((offsetX, offsetY));

def onUpdate(view, dt):
	isUpdate = True;
	if view.params["trigger"]:
		isUpdate = hasattr(view, "m_isTriggered") and view.m_isTriggered or False;
	if isUpdate:
		updateParams = view.params.get("update", {});
		updateType = updateParams.get("type", "");
		# 移动view
		if updateType == "move":
			if "speed" in updateParams:
				speedX, speedY = updateParams["speed"];
				view.rect.move_ip((speedX * dt/1000, speedY * dt/1000));
				if "return" in updateParams:
					x0, x1, y0, y1 = updateParams["return"];
					if 0 <= view.rect.left < x0:
						view.rect.left = x0;
						updateParams["speed"][0] = -updateParams["speed"][0];
					elif 0 <= x1 < view.rect.left:
						view.rect.left = x1;
						updateParams["speed"][0] = -updateParams["speed"][0];
					if 0 <= view.rect.top < y0:
						view.rect.top = y0;
						updateParams["speed"][1] = -updateParams["speed"][1];
					elif 0 <= y1 < view.rect.top:
						view.rect.top = y1;
						updateParams["speed"][1] = -updateParams["speed"][1];
		elif updateType == "rotate":
			if "speed" in updateParams:
				rotate = updateParams["speed"] * dt/1000;
				view.rotateBy(rotate);
				if "anchor" in updateParams:
					anchor = updateParams["anchor"];
					pos = view.rect.center;
					if hasattr(view, "m_rotatePos"):
						pos = view.m_rotatePos;
					rCos, rSin = math.cos(rotate*math.pi/180), math.sin(rotate*math.pi/180);
					anchorX = (pos[0] - anchor[0]) * rCos - (pos[1] - anchor[1]) * rSin + anchor[0];
					anchorY = (pos[0] - anchor[0]) * rSin + (pos[1] - anchor[1]) * rCos + anchor[1];
					# 更细位置
					view.m_rotatePos = (anchorX, anchorY);
					view.rect.center = view.m_rotatePos;

		# 销毁view
		if updateParams.get("kill", "") == "top":
			if view.rect.top <= -view.rect.height:
				view.kill();

SpriteConfig = {
	"guy" : [
		{"pos" : (0, 0), "size" : (40, 40)}
	],
	"cloud" : [
		{"pos" : (0, 176), "size" : (820, 40)},
		{"pos" : (60, 392), "size" : (820, 40)},
		{"pos" : (0, 608), "size" : (820, 40)},
		{"pos" : (60, 824), "size" : (820, 40)},
		{"pos" : (0, 1040), "size" : (1820, 40)}, # 底部
		{"pos" : (980, 176), "size" : (820, 40)},
		{"pos" : (920, 392), "size" : (820, 40)},
		{"pos" : (980, 608), "size" : (820, 40)},
		{"pos" : (920, 824), "size" : (820, 40)},
		{"pos" : (880, 0), "size" : (40, 864)}, # 中部
		{"pos" : (1800, 176), "size" : (40, 904)}, # 右部
	],
	"splinter" : [
		{
			"pos" : (600, 136), "size" : (80, 40),
		},
		{
			"pos" : (880, 56), "size" : (40, 80), "visible" : False,
			"trigger" : (840, 96, 40, 80),
			"update" : {
				"visible" : True,
				"offset" : (-40, 0),
			},
			"onTrigger" : onTrigger,
			"onUpdate" : onUpdate,
		},
		{
			"pos" : (680, 352), "size" : (80, 40),
		},
		{
			"pos" : (60, 352), "size" : (80, 40),
			"update" : {
				"type" : "move",
				"speed" : [800, 0],
				"return" : (60, 460, -1, -1),
			},
			"onUpdate" : onUpdate,
		},
		{
			"pos" : (460, 352), "size" : (80, 40),
			"update" : {
				"type" : "move",
				"speed" : [-800, 0],
				"return" : (60, 460, -1, -1),
			},
			"onUpdate" : onUpdate,
		},
		{
			"pos" : (880, 352), "size" : (40, 40),
			"update" : {
				"type" : "rotate",
				"anchor" : (400, 352),
				"speed" : 1000,
			},
			"onUpdate" : onUpdate,
		},
		# {
		# 	"pos" : (1880, 1080), "size" : (40, 40),
		# 	"trigger" : (1840, 200, 80, 40),
		# 	"update" : {
		# 		"type" : "move",
		# 		"speed" : [0, -1000],
		# 		"kill" : "top",
		# 	},
		# 	"onTrigger" : onTrigger,
		# 	"onUpdate" : onUpdate,
		# },
		# {
		# 	"pos" : (1840, 1080), "size" : (40, 40),
		# 	"trigger" : (1840, 800, 80, 40),
		# 	"update" : {
		# 		"type" : "move",
		# 		"speed" : [0, -1000],
		# 		"kill" : "top",
		# 	},
		# 	"onTrigger" : onTrigger,
		# 	"onUpdate" : onUpdate,
		# },
	],
};

class Scene1(_GG("BaseScene")):
	"""docstring for Scene1"""
	def __init__(self, size, params = {}):
		super(Scene1, self).__init__(size, params = params);
		self.__guys = pygame.sprite.Group();
		self.__sprites = pygame.sprite.Group();
		self.__clouds = pygame.sprite.Group();
		self.__splinters = pygame.sprite.Group();
		self.__splinterList = [];
		self.create();

	def create(self):
		# 创建背景
		self.background = pygame.image.load(os.path.join(_GG("g_AssetsPath"), "resource", "image", "background1.png")).convert();
		# 创建主角
		for cfg in SpriteConfig["guy"]:
			guy = Guy(params = cfg);
			self.addChild(guy);
			self.__guys.add(guy);
			self.__sprites.add(guy);
		# 创建云朵
		for cfg in SpriteConfig["cloud"]:
			cloud = Cloud(params = cfg);
			self.addChild(cloud);
			self.__clouds.add(cloud);
			self.__sprites.add(cloud);
		# 创建尖刺
		for cfg in SpriteConfig["splinter"]:
			splinter = Splinter(params = cfg);
			self.addChild(splinter);
			self.__splinters.add(splinter);
			self.__sprites.add(splinter);
			self.__splinterList.append(splinter);
		pass;

	def start(self):
		pass;

	def update(self, dt):
		for splinter in self.__splinterList:
			splinter.trigger([guy.rect.topleft for guy in self.__guys.sprites()]);
		self.updateGuySprite(dt);
		pass;

	def updateGuySprite(self, dt):
		splinterMap = pygame.sprite.groupcollide(self.__guys, self.__splinters, True, False);
		for guy in splinterMap:
			self.rmChild(guy, True);
		cloudMap = pygame.sprite.groupcollide(self.__guys, self.__clouds, False, False);
		for guy in self.__guys.sprites():
			if guy.rect.bottom >= _GG("SceneManager").getScreenSize()[1]:
				self.rmChild(guy, True);
				break;
			guy.collide(cloudMap.get(guy, [])); # 检测碰撞
