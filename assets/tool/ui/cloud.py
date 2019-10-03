import pygame;

class Cloud(pygame.sprite.Sprite):
	"""docstring for Cloud"""
	def __init__(self, params = {}):
		self.initParams(params);
		super(Cloud, self).__init__();
		self.image = pygame.Surface(self.__params["size"]);
		self.image.fill(self.__params["bgColor"]);
		self.rect = self.image.get_rect()

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : (25, 25),
			"bgColor" : (255,255,255),
		};
		for k,v in params.items():
			self.__params[k] = v;