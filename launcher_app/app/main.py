import os
import sys

from launcher_app.app.views.main import App
from launcher_app.app.utilities.auth import AuthManager


def main(server=None, **kwargs):
    redirect_path = os.getenv("TRAME_REDIRECT_PATH", "/redirect")
    auth_manager = AuthManager()
    auth_manager.start_session(redirect_path)
    app = App(server)
    for arg in sys.argv[1:]:
        try:
            key, value = arg.split("=")
            kwargs[key] = int(value)
        except:
            pass
    app.server.start(**kwargs)
