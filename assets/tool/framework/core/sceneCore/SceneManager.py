import os;
import pygame;

from _Global import _GG;
from function.base import *;

from sceneCore.HotKeyMap import *;

# 场景管理器
class SceneManager(object):
    def __init__(self):
        super(SceneManager, self).__init__();
        self._className_ = SceneManager.__name__;
        self.__screen = None;
        self.__isRunning = False;
        self.__sceneMap = {};
        self.__runningScene = None;
        self.__isFullScreen = False;

    def createScreen(self):
        self.__isFullScreen = True;
        self.__screen = pygame.display.set_mode(_GG("GameConfig").PjConfig().Get("winSize"), flags = pygame.FULLSCREEN);
        self.__isRunning = True;

    def getScreen(self):
        return self.__screen;

    def isRunning(self):
        return self.__isRunning;

    def destroyScreen(self):
        self.__screen = None;
        self.__isRunning = False;

    def run(self, init = None):
        self.createScreen();
        dt = pygame.time.Clock().tick();
        if callable(init):
            init();
        while self.isRunning():
            self.update(dt);
            dt = pygame.time.Clock().tick(_GG("GameConfig").PjConfig().Get("fps", 120));

    def update(self, dt):
        for event in pygame.event.get():
            eventId = GetEventIdByEventType(event.type);
            if eventId:
                _GG("EventDispatcher").dispatch(eventId, {"dt" : dt});
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.__isFullScreen = not self.__isFullScreen;
                    if self.__isFullScreen:
                        pygame.display.set_mode(_GG("GameConfig").PjConfig().Get("winSize"), flags = pygame.FULLSCREEN);
                    else:
                        pygame.display.set_mode(_GG("GameConfig").PjConfig().Get("winSize"));
                else:
                    eventId = GetEventIdByEventKey(event.key);
                    if eventId:
                        _GG("EventDispatcher").dispatch(eventId, {"dt" : dt});
            elif event.type == pygame.QUIT:
                self.destroyScreen();
                return;
        pygame.event.pump();
        if self.__runningScene and hasattr(self.__runningScene, "update"):
            self.__runningScene.update(dt);
        pygame.display.update();

    def createScene(self, name, sceneObj, *argList, **argDict):
        scene = None;
        if name in self.__sceneMap:
            _GG("Log").e(f"Error to create Scene! Err[Existed scene named '{name}'!]");
            return scene;
        try:
            scene = sceneObj(*argList, **argDict);
            scene._scene_name_ = name;
            self.__sceneMap[name] = scene;
        except Exception as e:
            _GG("Log").e(f"Error to create Scene! Err[{e}]");
        return scene;

    def runScene(self, name):
        runningScene = self.__runningScene;
        if runningScene and hasattr(runningScene, "stop"):
            runningScene.stop();
        if name not in self.__sceneMap:
            _GG("Log").e(f"Error to run Scene! Err[No exist scene named '{name}'!]");
            return;
        scene = self.__sceneMap[name];
        if not hasattr(scene, "_is_started_scene_") or not scene._is_started_scene_:
            if hasattr(scene, "start"):
                scene.start();
            scene._is_started_scene_ = True;
        self.__runningScene = scene;

    def destoryScene(self, name):
        if name not in self.__sceneMap:
            _GG("Log").e(f"Error to destory Scene! Err[No exist scene named '{name}'!]");
            return;
        scene = self.__sceneMap.pop(name);
        if scene == self.__runningScene:
            self.__runningScene = None;
        if hasattr(scene, "destory"):
            scene.destory();
        scene._is_started_scene_ = False;
        # 移除场景
        del scene;

    def getRunningScene(self):
        return self.__runningScene;