import pygame;

from _Global import _GG;

# 定时器对象
class BaseScene(pygame.sprite.Sprite):
    def __init__(self, size, params = {}):
        super(BaseScene, self).__init__();
        self.__initParams__(params);
        self.__surf = pygame.Surface(size);
        self.__surf.fill(self.__params["bgColor"]);
        self.__children = [];
        self.visible = self.__params["visible"];
        self.background = self.__params["background"];

    def __initParams__(self, params):
        # 初始化参数
        self.__params = {
            "bgColor" : (255,255,255),
            "visible" : True,
            "background" : None,
        };
        for k,v in params.items():
            self.__params[k] = v;

    @property
    def params(self):
        return self.__params;

    @property
    def surf(self):
        return self.__surf;

    @property
    def visible(self):
        return self.__visible;

    @visible.setter
    def visible(self, visible):
        self.__visible = bool(visible);

    @property
    def children(self):
        return self.__children;

    @property
    def background(self):
        return self.__background;

    @background.setter
    def background(self, bg):
        self.__background = bg;

    # 更新view
    def __call__(self, *argList, **argDict):
        if not self.visible:
            return;
        # 执行更新逻辑
        if hasattr(self, "update"):
            self.update(*argList, **argDict);
        # 更新子节点
        for child in self.__children:
            if callable(child):
                child(*argList, **argDict);
            elif hasattr(child, "update"):
                child.update(*argList, **argDict);
        # 更新布局
        self.layout();
        pass;

    def addChild(self, child):
        child.parent = self;
        self.__children.append(child);

    def rmChild(self, child, isKill = False):
        if child in self.__children:
            child.visible = False;
            self.__children.remove(child);
            if isKill:
                child.clearTempGroups();
                child.kill();
        pass;

    def layout(self):
        if self.__background:
            self.__surf.blit(self.__background, (0, 0)); # 更新背景
        for child in self.__children:
            if not child.visible:
                continue;
            self.__surf.blit(child.surf, child.rect);