import pygame;

from _Global import _GG;

class Splinter(_GG("BaseView")):
	"""docstring for Splinter"""
	def __init__(self, params = {}):
		super(Splinter, self).__init__(params = self.initParams(params));
		self.__trigger = None;
		self.initTrigger();

	def initParams(self, params):
		# 初始化参数
		default = {
			"pos" : (0, 0),
			"size" : (25, 25),
			"bgColor" : (255,0,0),
			"trigger" : [],
			"onTrigger" : None,
			"onUpdate" : None,
		};
		for k,v in params.items():
			default[k] = v;
		return default;

	def initTrigger(self, rect = []):
		if not rect:
			rect = self.params["trigger"];
		if rect:
			self.__trigger = pygame.Rect(*self.params["trigger"]);

	def trigger(self, posList):
		if self.__trigger:
			for pos in posList:
				if self.__trigger.collidepoint(pos):
					if callable(self.params["onTrigger"]):
						self.params["onTrigger"](self);
					break;
		pass;

	def update(self, dt):
		if callable(self.params["onUpdate"]):
			self.params["onUpdate"](self, dt);
		pass;