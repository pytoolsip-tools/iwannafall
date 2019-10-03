import pygame;

class Splinter(pygame.sprite.Sprite):
	"""docstring for Splinter"""
	def __init__(self, params = {}):
		self.initParams(params);
		super(Splinter, self).__init__();
        self.surf = pygame.Surface(self.__params["size"]);
        self.surf.fill(self.__params["bgColor"]);
        self.rect = self.surf.get_rect()

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : (25, 25),
			"bgColor" : (255,255,255),
		};
		for k,v in params.items():
			self.__params[k] = v;