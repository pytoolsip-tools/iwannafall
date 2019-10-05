import pygame;

from _Global import _GG;
from function.base import *;

from ui import *;

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
			"pos" : (200, 136), "size" : (40, 40), "visible" : False,
			# "trigger" : (1840, 200, 80, 40),
			# "anim" : {
			# 	"type" : "move",
			# 	"speed" : (0, -1000),
			# },
			# "kill" : "top",
		},
		{
			"pos" : (880, 136), "size" : (40, 40),
			"trigger" : (840, 96, 40, 80),
			# "anim" : {
			# 	"type" : "move",
			# 	"speed" : (0, -1000),
			# },
			# "kill" : "top",
		},
		# {
		# 	"pos" : (1880, 1080), "size" : (40, 40),
		# 	"trigger" : (1840, 200, 80, 40),
		# 	"anim" : {
		# 		"type" : "move",
		# 		"speed" : (0, -1000),
		# 	},
		# 	"kill" : "top",
		# },
		# {
		# 	"pos" : (1840, 1080), "size" : (40, 40),
		# 	"trigger" : (1840, 800, 80, 40),
		# 	"anim" : {
		# 		"type" : "move",
		# 		"speed" : (0, -1000),
		# 	},
		# 	"kill" : "top",
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
		pass;

	def start(self):
		pass;

	def update(self, dt):
		for splinter in self.__splinters.sprites():
			splinter.onTrigger([guy.rect.topleft for guy in self.__guys.sprites()]);
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