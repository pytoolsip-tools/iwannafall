# 定时器对象
class Timer(object):
    def __init__(self, duration, callback, tickCount = -1, stopCallback = None):
        super(Timer, self).__init__();
        self.__duration = duration;
        self.__callback = callback;
        self.__tickCount = tickCount;
        self.__stopCallback = stopCallback;
        self.__pass = 0;
        self.__tickedCount = 0;
        self.__isPause = False;
    
    def update(self, dt):
        if self.__isPause:
            return;
        self.__pass += dt;
        if self.__pass >= self.__duration:
            if callable(self.__callback):
                self.__callback(self.__pass);
            self.__pass = 0;
            self.__tickedCount += 1;
            if self.__tickCount > 0 and self.__tickedCount >= self.__tickCount:
                self.stop();
        pass;

    def stop(self):
        self.pause();
        if callable(self.__stopCallback):
            self.__stopCallback(self);
        pass;

    def pause(self):
        self.__isPause = True;

    def start(self):
        self.__isPause = False;