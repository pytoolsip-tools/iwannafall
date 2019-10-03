import sys,os;
import pygame;

# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
# 添加搜索路径
if CURRENT_PATH not in sys.path:
	sys.path.append(CURRENT_PATH);

# 导入加载模块
from framework._load import Loader;

# 获取工程路径
pjPath = os.path.dirname(CURRENT_PATH);
if len(sys.argv) > 1:
	pjPath = sys.argv[1];

# 初始化加载器
Loader = Loader(CURRENT_PATH, pjPath);
Loader.loadGlobalInfo();
Loader.verifyDefaultData();
Loader.lockGlobal();

from _Global import _GG;

if __name__ == '__main__':
    pygame.init();
    pygame.display.set_mode(_GG("GameConfig").PjConfig().Get("winSize", (1080, 720)));
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0);
    pygame.quit();