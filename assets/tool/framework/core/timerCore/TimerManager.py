# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-01-13 22:29:38
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-14 17:32:19

from timerCore.Timer import *;

class TimerManager(object):
	def __init__(self):
		super(TimerManager, self).__init__();
		self.__timerList = {};
		self.__tempTimerList = {};

	def __onStopTimer__(self, timer):
		if timer in self.__timerList:
			self.__timerList.remove(timer);
		if timer in self.__tempTimerList:
			self.__tempTimerList.remove(timer);

	def create(self, duration, callback, tickCount = -1):
		timer = Timer(duration, callback, tickCount, self.__onStopTimer__);
		self.__tempTimerList.append(timer);
		return timer;

	def delete(self, timer):
		if timer in self.__timerList:
			timer.Stop();

	def clear(self):
		for timer in self.__timerList:
			timer.Stop();

	def update(self, dt):
		for timer in self.__tempTimerList:
			self.__timerList.append(timer);
		self.__tempTimerList.clear();
		for timer in self.__timerList:
			timer.update(dt);