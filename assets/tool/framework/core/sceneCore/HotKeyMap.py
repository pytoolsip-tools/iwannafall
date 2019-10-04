import pygame;

from _Global import _GG;

__hot_key_map = {
    pygame.K_ESCAPE : "K_ESC",
    pygame.K_SPACE  : "K_SPACE",
    # pygame.K_LEFT   : "K_LEFT",
    # pygame.K_UP     : "K_UP",
    # pygame.K_RIGHT  : "K_RIGHT",
    # pygame.K_DOWN   : "K_DOWN",
};

__hot_type_map = {
    # pygame.JOYAXISMOTION : "JOYAXISMOTION",
    # pygame.JOYBALLMOTION : "JOYBALLMOTION",
    pygame.JOYBUTTONDOWN : "JOYBUTTONDOWN",
    # pygame.JOYBUTTONUP : "JOYBUTTONUP",
    # pygame.JOYHATMOTION : "JOYHATMOTION",
};

# 根据按键类型，获取事件ID
def GetEventIdByEventKey(key):
    if key in __hot_key_map:
        eKey = __hot_key_map[key];
        if hasattr(_GG("EVENT_ID"), eKey):
            return getattr(_GG("EVENT_ID"), eKey);
    return None;

def GetEventIdByEventType(key):
    if key in __hot_type_map:
        tKey = __hot_type_map[key];
        if hasattr(_GG("EVENT_ID"), tKey):
            return getattr(_GG("EVENT_ID"), tKey);
    return None;