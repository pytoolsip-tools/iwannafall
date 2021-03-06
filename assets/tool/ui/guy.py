import math;
import pygame;

from _Global import _GG;
from function.base import *;

def getRegisterEventMap(G_EVENT):
	return {
		G_EVENT.K_SPACE : "jump",
		G_EVENT.JOYBUTTONDOWN : "checkJump",
	};

class Guy(_GG("BaseView")):
	"""docstring for Guy"""
	def __init__(self, params = {}):
		super(Guy, self).__init__(params = self.initParams(params));
		self.registerEventMap();
		self.__id = self.params["id"];
		self.__jumpCnt = self.params["jump"]["count"]; # 跳跃次数
		self.__speed = 0; # 自由落体速率
		self.__walkSpeed = 0; # 移动速率

	def __del__(self):
		self.unregisterEventMap();

	def initParams(self, params):
		# 初始化参数
		default = {
			"id" : 0,
			"pos" : (0, 0),
			"size" : (25, 25),
			"bgColor" : (0,255,0),
			"jump" : {
				"count" : 2,
				"gravity" : 40,
				"factor" : 100,
				"velocity" : -10,
				"limit" : 16,
			},
			"walk" : {
				"acceleration" : 100, # 加速度
				"limit" : 5, # 限速
				"factor" : 100,
			},
			"collideOffset" : 1,
			"axisError" : 0.01,
		};
		for k,v in params.items():
			default[k] = v;
		return default;

	def registerEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").register(eventId, self, callbackName);

	def unregisterEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").unregister(eventId, self, callbackName);

	def jump(self, data = {}):
		jumpParams = self.params["jump"];
		if self.__jumpCnt >= jumpParams["count"]:
			return;
		self.__jumpCnt += 1;
		self.__speed = jumpParams["velocity"];
		self.rect.move_ip((0, jumpParams["velocity"]));
		self.layout();

	def stand(self):
		self.__jumpCnt = 0;
		self.__speed = 0;

	def isStanding(self):
		return self.__jumpCnt == 0 and self.__speed == 0;

	def stay(self):
		self.__walkSpeed = 0;

	def isStaying(self):
		if self.__walkSpeed > 0:
			return False;
		# 判断键盘事件
		pressedKey = pygame.key.get_pressed();
		for k in [pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT]:
			if pressedKey[k]:
				return False;
		# 判断手柄位移
		if self.__id < pygame.joystick.get_count():
			joystick = pygame.joystick.Joystick(self.__id);
			if joystick.get_numaxes() > 0:
				if math.fabs(joystick.get_axis(0)) > self.params["axisError"]: # 抖动误差值
					return False;
		return True;

	def update(self, dt, sprites = []):
		self.walk(dt);
		self.fall(dt);
		pass;

	def fall(self, dt):
		jumpParams = self.params["jump"];
		self.__speed += jumpParams["gravity"] * dt/1000;
		if math.fabs(self.__speed) > jumpParams["limit"]:
			self.__speed = self.__speed / math.fabs(self.__speed) * jumpParams["limit"];
		self.rect.move_ip((0, self.__speed * jumpParams["factor"] * dt/1000));

	def walk(self, dt):
		direction = self.getDirection();
		# 判断方向事件
		if direction == -1:
			if self.__walkSpeed > 0:
				self.stay();
		elif direction == 1:
			if self.__walkSpeed < 0:
				self.stay();
		else:
			self.stay();
		if direction != 0:
			# 更新速度
			walkParams = self.params["walk"];
			self.__walkSpeed += direction * walkParams["acceleration"] * dt/1000;
			if math.fabs(self.__walkSpeed) > walkParams["limit"]:
				self.__walkSpeed = direction * walkParams["limit"];
			self.rect.move_ip((self.__walkSpeed * walkParams["factor"] * dt/1000, 0));

	def layout(self):
		_GG("SceneManager").getScreen().blit(self.image, self.rect);
		pass;

	def collide(self, sprites = []):
		def updateLeft(val):
			self.rect.left = val;
			self.stay();
			pass;
		def updateRight(val):
			self.rect.right = val;
			self.stay();
			pass;
		def updateTop(val):
			self.rect.top = val;
			self.__speed = 0;
			pass;
		def updateBottom(val):
			self.rect.bottom = val + self.params["collideOffset"];
			self.stand();
			pass;
		# 判断碰撞的精灵
		for sprite in sprites:
			spriteRect = sprite.rect;
			# 存在8种碰撞情况
			if self.rect.left <= spriteRect.left <= self.rect.right:
				diffX = self.rect.right - spriteRect.left;
				# 3种情况
				if self.rect.top <= spriteRect.top and diffX >= self.rect.bottom - spriteRect.top:
					updateBottom(spriteRect.top);
				elif self.rect.bottom >= spriteRect.bottom and diffX >= spriteRect.bottom - self.rect.top:
					updateTop(spriteRect.bottom);
				else:
					updateRight(spriteRect.left);
			elif self.rect.left <= spriteRect.right <= self.rect.right:
				diffX = spriteRect.right - self.rect.left;
				# 3种情况
				if self.rect.top <= spriteRect.top and diffX >= self.rect.bottom - spriteRect.top:
					updateBottom(spriteRect.top);
				elif self.rect.bottom >= spriteRect.bottom and diffX >= spriteRect.bottom - self.rect.top:
					updateTop(spriteRect.bottom);
				else:
					updateLeft(spriteRect.right);
			elif self.rect.top <= spriteRect.top <= self.rect.bottom: # 1种情况
				updateBottom(spriteRect.top);
			elif self.rect.top <= spriteRect.bottom <= self.rect.bottom: # 1种情况
				updateTop(spriteRect.bottom);
		# 判断屏幕横向边界
		if self.rect.left < 0:
			updateLeft(0);
		elif self.rect.right > _GG("SceneManager").getScreenSize()[0]:
			updateRight(_GG("SceneManager").getScreenSize()[0]);
		pass;

	def getDirection(self):
		# 检测键盘按键
		pressedKey = pygame.key.get_pressed();
		if pressedKey[pygame.K_a] or pressedKey[pygame.K_LEFT]:
			return -1;
		elif pressedKey[pygame.K_d] or pressedKey[pygame.K_RIGHT]:
			return 1;
		# 检测手柄
		if self.__id < pygame.joystick.get_count():
			joystick = pygame.joystick.Joystick(self.__id);
			if joystick.get_numaxes() > 0:
				axis = joystick.get_axis(0);
				if math.fabs(axis) > self.params["axisError"]: # 抖动误差值
					return axis < 0 and -1 or 1;
		return 0;

	def checkJump(self, data = {}):
		if self.__id < pygame.joystick.get_count():
			joystick = pygame.joystick.Joystick(self.__id);
			if joystick.get_numbuttons() > 0:
				if joystick.get_button(0) == 1:
					self.jump();
		pass;