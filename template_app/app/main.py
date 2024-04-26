import sys

from .core import App
from .auth import TrameAuth


def main(server=None, **kwargs):
    TrameAuth.start_session("/redirect")
    app = App(server)
    for arg in sys.argv[1:]:
        try:
            key, value = arg.split("=")
            kwargs[key] = int(value)
        except:
            pass
    app.server.start(**kwargs)
