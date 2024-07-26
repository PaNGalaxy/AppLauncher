import json
import logging
from launcher_app.app.config import TRAME_LAUNCHER_TOOL_PATH

class ToolModel:

    def __init__(self):
        try:
            self.tools = json.load(open(TRAME_LAUNCHER_TOOL_PATH, "r"))
        except:
            logging.error(f"Could not load tools from provided path: {TRAME_LAUNCHER_TOOL_PATH}")
            self.tools = {}

    def get_tools(self, as_list=False):
        if as_list:
            return [
                tool
                for category in self.tools.values()
                for tool in category.get("tools", [])
            ]
        return self.tools
