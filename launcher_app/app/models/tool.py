import json
from pathlib import Path

TOOL_PATH = Path("launcher_app/app/tools.json")


class ToolModel:

    def __init__(self):
        self.tool_list = json.load(open(TOOL_PATH, "r"))

    def get_tools(self):
        return self.tool_list


