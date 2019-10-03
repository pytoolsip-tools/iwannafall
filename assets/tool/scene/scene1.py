import pygame;

from _Global import _GG;
from function.base import *;

from ui import *;

SpriteConfig = {
	"guy" : (0, 0),
	"cloud" : [
		[(0, 200), (300, 20)],
		[(400, 400), (300, 20)],
		[(800, 400), (40, 20)],
		[(840, 220), (20, 200)],
		[(840, 200), (500, 20)],
	],
};

class Scene1(object):
	"""docstring for Scene1"""
	def __init__(self, params = {}):
		super(Scene1, self).__init__();
		self.__sprites = pygame.sprite.Group();
		self.__clouds = pygame.sprite.Group();
		self.__splinters = pygame.sprite.Group();
		self.create();

	def create(self):
		# 创建背景
		self.__background = pygame.image.load(os.path.join(_GG("g_AssetsPath"), "resource", "image", "background1.png")).convert();
		# 创建主角
		self.__guy = Guy();
		# 创建云朵
		for i in range(5):
			cloud = Cloud(params = {"size" : SpriteConfig["cloud"][i][1]});
			self.__clouds.add(cloud);
			self.__sprites.add(cloud);
		# 创建尖刺
		for i in range(5):
			splinter = Splinter();
			self.__splinters.add(splinter);
			self.__sprites.add(splinter);
		pass;

	def start(self):
		# 初始化精灵位置
		self.__guy.rect.topleft = SpriteConfig["guy"];
		for i, cloud in enumerate(self.__clouds.sprites()):
			cloud.rect.topleft = SpriteConfig["cloud"][i][0];

	def update(self, dt):
		_GG("SceneManager").getScreen().blit(self.__background, (0, 0)); # 更新背景
		self.__sprites.update(dt);
		self.__sprites.draw(_GG("SceneManager").getScreen());
		self.updateGuySprite(dt);
		pass;

	def updateGuySprite(self, dt):
		self.__guy.update(dt, pygame.sprite.spritecollide(self.__guy, self.__clouds, False));
		self.__guy.layout();