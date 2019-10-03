import pygame;

from _Global import _GG;
from function.base import *;

from ui import *;

class Scene1(object):
	"""docstring for Scene1"""
	def __init__(self, params = {}):
		super(Scene1, self).__init__();
		self.__sprites = pygame.sprite.Group();
		self.__clouds = pygame.sprite.Group();
		self.__splinters = pygame.sprite.Group();
		self.create();

	def create(self):
		# 创建主角
		self.__guy = Guy();
		self.__sprites.add(self.__guy);
		# 创建云朵
		for i in range(10):
			cloud = Cloud();
			self.__clouds.add(cloud);
			self.__sprites.add(cloud);
		# 创建尖刺
		for i in range(10):
			splinter = Splinter();
			self.__splinters.add(splinter);
			self.__sprites.add(splinter);
		pass;

	def start(self):
		self.__guy.rect.topleft = (100,200);
		self.__clouds.sprites()[0].rect.topleft = (200,400);

	def update(self, dt):
		self.__sprites.update(dt);
		self.__sprites.draw(_GG("SceneManager").getScreen());
		pass;