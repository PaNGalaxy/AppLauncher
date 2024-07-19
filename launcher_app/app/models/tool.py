import json
import logging
import os

TOOL_PATH = os.getenv("TRAME_LAUNCHER_TOOL_PATH", "launcher_app/app/tools.json")


class ToolModel:

    def __init__(self):
        try:
            self.tools = json.load(open(TOOL_PATH, "r"))
        except:
            logging.error(f"Could not load tools from provided path: {TOOL_PATH}")
            self.tools = {}

    def get_tools(self, as_list=False):
        if as_list:
            return [
                tool
                for category in self.tools.values()
                for tool in category.get("tools", [])
            ]
        return self.tools
