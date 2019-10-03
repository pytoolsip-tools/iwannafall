import pygame;

class Guy(pygame.sprite.Sprite):
	"""docstring for Guy"""
	def __init__(self, params = {}):
		self.initParams(params);
		super(Guy, self).__init__();
		self.image = pygame.Surface(self.__params["size"]);
		self.image.fill(self.__params["bgColor"]);
		self.rect = self.image.get_rect()
		self.__jumpCnt = 0; # 跳跃次数

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : (25, 25),
			"bgColor" : (255,255,255),
			"jumpCount" : 2,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def jump(self):
		if self.__jumpCnt >= self.__params["jumpCount"]:
			return;
		self.__jumpCnt += 1;

	def reset(self):
		self.__jumpCnt = 0;

	def update(self, dt):
		pass;