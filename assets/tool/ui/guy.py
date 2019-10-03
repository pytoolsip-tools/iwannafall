import pygame;

from _Global import _GG;
from function.base import *;

Direction = {
	"LEFT" : -1,
	"UP" : -1,
	"RIGHT" : 1,
	"DOWN" : 1,
};

def getRegisterEventMap(G_EVENT):
	return {
		G_EVENT.K_SPACE : "jump",
	};

class Guy(pygame.sprite.Sprite):
	"""docstring for Guy"""
	def __init__(self, params = {}):
		self.initParams(params);
		super(Guy, self).__init__();
		self.image = pygame.Surface(self.__params["size"]);
		self.image.fill(self.__params["bgColor"]);
		self.rect = self.image.get_rect()
		self.registerEventMap();
		self.__jumpCnt = self.__params["jumpCount"]; # 跳跃次数
		self.__speed = 0; # 自由落体速率

	def __del__(self):
		self.unregisterEventMap();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : (25, 25),
			"bgColor" : (255,255,255),
			"jumpCount" : 2,
			"gravity" : 40,
			"factor" : 1,
			"velocity" : -12,
			"walkSpeed" : 0.5,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def registerEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").register(eventId, self, callbackName);

	def unregisterEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").unregister(eventId, self, callbackName);

	def jump(self, data = {}):
		if self.__jumpCnt >= self.__params["jumpCount"]:
			return;
		self.__jumpCnt += 1;
		self.__speed = self.__params["velocity"];
		self.rect.move_ip((0, self.__params["velocity"]));
		self.layout();

	def stand(self):
		self.__jumpCnt = 0;
		self.__speed = 0;

	def isStanding(self):
		return self.__jumpCnt == 0 and self.__speed == 0;

	def isStaying(self):
		pressedKey = pygame.key.get_pressed();
		for k in [pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT]:
			if pressedKey[k]:
				return False;
		return True;

	def update(self, dt, sprites = []):
		isStay, isStand = self.collide(sprites);
		if not isStay:
			self.walk(dt);
		if not isStand:
			self.fall(dt);
		pass;

	def fall(self, dt):
		self.__speed += self.__params["gravity"] * dt/1000;
		self.rect.move_ip((0, self.__speed*self.__params["factor"]));

	def walk(self, dt):
		pressedKey = pygame.key.get_pressed();
		if pressedKey[pygame.K_a] or pressedKey[pygame.K_LEFT]:
			self.rect.move_ip((-dt * self.__params["walkSpeed"], 0));
		elif pressedKey[pygame.K_d] or pressedKey[pygame.K_RIGHT]:
			self.rect.move_ip((dt * self.__params["walkSpeed"], 0));

	def layout(self):
		_GG("SceneManager").getScreen().blit(self.image, self.rect);
		pass;

	def collide(self, sprites = []):
		isStay, isStand = self.isStaying(), self.isStanding();
		def updateTop(val):
			self.rect.top = spriteRect.bottom;
			self.__speed = 0;
			pass;
		def updateBottom(val):
			self.rect.bottom = val;
			self.stand();
			isStand = True;
			pass;
		for sprite in sprites:
			spriteRect = sprite.rect;
			# 存在8种碰撞情况
			if self.rect.left <= spriteRect.left <= self.rect.right:
				diffX, diffY = self.rect.right - spriteRect.left, self.rect.width;
				# 3种情况
				if self.rect.top <= spriteRect.top and diffX >= self.rect.bottom - spriteRect.top:
					updateBottom(spriteRect.top);
				elif self.rect.bottom >= spriteRect.bottom and diffX >= spriteRect.bottom - self.rect.top:
					updateTop(spriteRect.bottom);
				else:
					self.rect.right = spriteRect.left;
					isStay = True;
			elif self.rect.left <= spriteRect.right <= self.rect.right:
				diffX, diffY = spriteRect.right - self.rect.left, self.rect.width;
				# 3种情况
				if self.rect.top <= spriteRect.top and diffX >= self.rect.bottom - spriteRect.top:
					updateBottom(spriteRect.top);
				elif self.rect.bottom >= spriteRect.bottom and diffX >= spriteRect.bottom - self.rect.top:
					updateTop(spriteRect.bottom);
				else:
					self.rect.left = spriteRect.right;
					isStay = True;
			elif self.rect.top <= spriteRect.top <= self.rect.bottom: # 1种情况
				updateBottom(spriteRect.top);
			elif self.rect.top <= spriteRect.bottom <= self.rect.bottom: # 1种情况
				updateTop(spriteRect.bottom);
		return isStay, isStand;
		