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

SceneManager = Loader.getSceneManager();

from scene.scene1 import Scene1;

def initFunc():
    SceneManager.createScene("mainScene", Scene1);
    SceneManager.runScene("mainScene");

if __name__ == '__main__':
    pygame.init();
    # 初始化手柄事件
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i);
        joystick.init();
    # 运行场景
    SceneManager.run(init = initFunc);
    pygame.quit();