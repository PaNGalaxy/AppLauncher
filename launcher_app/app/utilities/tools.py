import json
from pathlib import Path

TOOL_PATH = Path("launcher_app/app/tools.json")


def get_tools():
    return json.load(open(TOOL_PATH, "r"))


