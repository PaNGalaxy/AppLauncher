from py_mvvm.trame_binding import TrameBinding

from trame.app import get_server
from trame.decorators import TrameApp
from trame.widgets import router

from launcher_app.app.mvvm_factory import create_viewmodels
from launcher_app.app.utilities.auth import AuthManager
from launcher_app.app.views.theme import ThemedApp
from launcher_app.app.views.view_controller import ViewController


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


@TrameApp()
class App(ThemedApp):
    def __init__(self, server=None):
        super().__init__(server=server)

        self.server = get_server(server, client_type="vue3")
        self.ctrl = self.server.controller
        binding = TrameBinding(self.server.state)
        self.vm = create_viewmodels(binding)
        self.auth = AuthManager()

        self.view_controller = ViewController(self.server, self.vm)

        self.create_ui()

    @property
    def state(self):
        return self.server.state

    def create_ui(self):
        self.state.trame__title = "Neutrons App Dashboard"

        with super().create_ui() as layout:
            with layout.content:
                router.RouterView()

                return layout
