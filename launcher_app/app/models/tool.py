import json
from pathlib import Path

TOOL_PATH = Path("launcher_app/app/tools.json")


class ToolModel:

    def __init__(self):
        self.tools = json.load(open(TOOL_PATH, "r"))

    def get_tools(self, as_list=False):
        if as_list:
            return [
                tool
                for category in self.tools.values()
                for tool in category.get("tools", [])
            ]
        return self.tools
