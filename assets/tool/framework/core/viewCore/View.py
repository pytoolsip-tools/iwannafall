import pygame;

# 定时器对象
class BaseView(pygame.sprite.Sprite):
    def __init__(self, params = {}):
        super(BaseView, self).__init__();
        self.__initParams__(params);
        self.__surf = pygame.Surface(self.__params["size"]);
        self.__surf.fill(self.__params["bgColor"]);
        self.rect = self.__surf.get_rect();
        self.rect.topleft = self.__params["pos"];
        self.__parent = None;
        self.__children = [];
        self.__tempGroups = [];
        self.visible = self.__params["visible"];
        self.scale = self.__params["scale"];
        self.rotate = self.__params["rotate"];
        self.background = self.__params["background"];

    def __initParams__(self, params):
        # 初始化参数
        self.__params = {
            "pos" : (0, 0),
            "size" : (25, 25),
            "bgColor" : (255,255,255),
            "visible" : True,
            "scale" : (1, 1),
            "rotate" : 0,
            "background" : None,
        };
        for k,v in params.items():
            self.__params[k] = v;

    @property
    def params(self):
        return self.__params;

    @property
    def parent(self):
        return self.__parent;

    @parent.setter
    def parent(self, parent):
        if self.__parent:
            self.__parent.remove(self);
        self.__parent = parent;

    @property
    def visible(self):
        return self.__visible;

    @visible.setter
    def visible(self, visible):
        self.__visible = bool(visible);
        if not self.__visible:
            for group in self.groups():
                self.remove(group);
                self.__tempGroups.append(group);
        else:
            for group in self.__tempGroups:
                self.add(group);
            self.clearTempGroups();
        pass;

    @property
    def surf(self):
        return self.__surf;

    @property
    def image(self):
        return self.surf;

    @property
    def children(self):
        return self.__children;

    @property
    def scale(self):
        return self.__scale;

    @scale.setter
    def scale(self, scale):
        if len(scale) < 2:
            return;
        x, y = scale[0], scale[1];
        pygame.transform.scale(self.surf, (x * self.rect.width, y * self.rect.height));
        self.__scale = (x, y);

    @property
    def rotate(self):
        return self.__rotate;

    @rotate.setter
    def rotate(self, angle):
        if not isinstance(angle, int):
            return;
        pygame.transform.rotate(self.surf, angle);
        self.__rotate = angle;

    @property
    def background(self):
        return self.__background;

    @background.setter
    def background(self, bg):
        self.__background = bg;

    def clearTempGroups(self):
        self.__tempGroups = [];

    def __checkVisible__(self):
        self.visible = self.visible;
        return self.visible;

    # 更新view
    def __call__(self, *argList, **argDict):
        if not self.__checkVisible__():
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

    def rmSelf(self, isKill = False):
        if self.__parent:
            self.__parent.rmChild(self);
        pass;

    def layout(self):
        if self.__background:
            self.surf.blit(self.__background, (0, 0)); # 更新背景
        for child in self.__children:
            if not child.visible:
                continue;
            self.surf.blit(child.surf, child.rect);