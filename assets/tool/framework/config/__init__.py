import os;
import sys;
import json;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
sys.path.append(CURRENT_PATH);

__all__ = ["TOOL_INFO", "initToolInfo", "GameConfig"];

# 工具信息
TOOL_INFO = {};
def initToolInfo():
    toolPath = os.path.join(CURRENT_PATH, "../tool.json");
    if os.path.exists(toolPath):
        with open(toolPath, "r") as f:
            TOOL_INFO = json.loads(f.read());
initToolInfo();

try:
	from game_config import GameConfig;

except Exception as e:
	raise e;
finally:
	sys.path.remove(CURRENT_PATH);