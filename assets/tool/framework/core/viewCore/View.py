import pygame;

# 定时器对象
class BaseView(pygame.sprite.Sprite):
    def __init__(self, params = {}):
        super(BaseView, self).__init__();
        self.__initParams__(params);
        self.__surf = pygame.Surface(self.__params["size"]);
        self.__surf.fill(self.__params["bgColor"]);
        self.rect = self.__surf.get_rect();
        self.__parent = None;
        self.__children = [];
        self.__tempGroups = [];
        self.visible = self.__params["visible"];
        self.anchor = self.__params["anchor"];
        self.pos = self.__params["pos"];
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
            "anchor" : (0, 0),
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

    @surf.setter
    def surf(self, surf):
        topleft = self.rect.topleft;
        self.__surf = surf;
        self.rect = self.__surf.get_rect();
        self.rect.topleft = topleft;

    @property
    def image(self):
        return self.surf;

    @property
    def children(self):
        return self.__children;

    @property
    def anchor(self):
        return self.__anchor;

    @anchor.setter
    def anchor(self, anchor):
        if isinstance(anchor, int) or isinstance(anchor, float):
            anchor = (anchor, anchor);
        if (isinstance(anchor, list) or isinstance(anchor, tuple)) and len(anchor) == 2:
            self.__anchor = (anchor[0], anchor[1]);

    @property
    def pos(self):
        return (self.rect.left + self.__anchor[0] * self.rect.width, self.rect.top + self.__anchor[1] * self.rect.height);

    @pos.setter
    def pos(self, pos):
        if (isinstance(pos, list) or isinstance(pos, tuple)) and len(pos) == 2:
            self.rect.topleft = (pos[0] - self.__anchor[0] * self.rect.width, pos[1] - self.__anchor[1] * self.rect.height);

    @property
    def size(self):
        return (self.rect.width, self.rect.height);

    @size.setter
    def size(self, size):
        if (isinstance(size, list) or isinstance(size, tuple)) and len(size) == 2:
            pos = self.pos;
            self.rect.width, self.rect.height = size[0], size[1];
            self.pos = pos;

    @property
    def scale(self):
        return self.__scale;

    @scale.setter
    def scale(self, scale):
        if isinstance(scale, int) or isinstance(scale, float):
            scale = (scale, scale);
        if (isinstance(scale, list) or isinstance(scale, tuple)) and len(scale) < 2:
            return;
        pos = self.pos;
        x, y = scale[0], scale[1];
        self.surf = pygame.transform.scale(self.surf, (int(x * self.rect.width), int(y * self.rect.height)));
        self.pos = pos;
        self.__scale = (x, y);

    @property
    def rotate(self):
        return self.__rotate;

    @rotate.setter
    def rotate(self, angle):
        if not isinstance(angle, int):
            return;
        pos = self.pos;
        self.surf = pygame.transform.rotate(self.surf, angle);
        self.pos = pos;
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