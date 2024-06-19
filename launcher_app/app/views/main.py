from py_mvvm.trame_binding import TrameBinding

from trame.decorators import TrameApp
from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame_client.widgets import html

from launcher_app.app.mvvm_factory import create_viewmodels
from .login import LogoutToolbar, LoginView
from .home import HomeView
from .theme import CustomComponents, ThemedApp
from ..utilities.auth import AuthManager


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------

@TrameApp()
class App(ThemedApp):
    def __init__(self, server=None):
        super().__init__(server)

        self.ctrl = self.server.controller
        binding = TrameBinding(self.server.state)
        self.home_vm, self.user_vm = create_viewmodels(binding)
        self.auth = AuthManager()

        self.create_ui()

    def create_ui(self):
        self.state.trame__title = "Single Crystal Diffraction Dashboard"
        with super().create_ui() as layout:
            layout.title.set_text("Single Crystal Diffraction Dashboard")
            with layout.toolbar:
                LogoutToolbar(self.user_vm)
            with layout.content:
                with vuetify.VContainer(classes="align-start d-flex justify-center mt-8"):
                    LoginView(self.user_vm)
                    HomeView(self.state, self.server, self.home_vm)