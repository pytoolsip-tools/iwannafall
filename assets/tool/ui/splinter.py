import pygame;

from _Global import _GG;

class Splinter(_GG("BaseView")):
	"""docstring for Splinter"""
	def __init__(self, params = {}):
		super(Splinter, self).__init__(params = self.initParams(params));
		self.__trigger = None;
		self.initTrigger();
		self.__isMoving = False;

	def initParams(self, params):
		# 初始化参数
		default = {
			"pos" : (0, 0),
			"size" : (25, 25),
			"bgColor" : (255,0,0),
			"trigger" : [],
			"anim" : {
				"type" : "",
				"speed" : (0, 0),
			},
			"kill" : "",
		};
		for k,v in params.items():
			default[k] = v;
		return default;

	def initTrigger(self, rect = []):
		if not rect:
			rect = self.params["trigger"];
		if rect:
			self.__trigger = pygame.Rect(*self.params["trigger"]);

	def update(self, dt, posList = []):
		self.onMove(dt);
		self.onKill();
		pass;

	def onTrigger(self, posList):
		if self.__trigger and not self.__isMoving:
			for pos in posList:
				if self.__trigger.collidepoint(pos):
					self.__isMoving = True;
					break;
		pass;

	def onMove(self, dt):
		if self.__isMoving:
			animParams = self.params["anim"];
			if animParams["type"] == "move":
				speedX, speedY = animParams["speed"];
				self.rect.move_ip((speedX * dt/1000, speedY * dt/1000));

	def onKill(self):
		if self.params["kill"] == "top":
			if self.rect.top <= -self.rect.height:
				self.kill();