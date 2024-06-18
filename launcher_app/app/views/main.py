import json
import logging
from pathlib import Path

from py_mvvm.trame_binding import TrameBinding

from sass import compile

from trame.app import get_server
from trame.decorators import TrameApp
from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame_client.widgets import html

from launcher_app.app.mvvm_factory import create_viewmodels
from launcher_app.app.views.base import SinglePageLayout
from .login import LogoutToolbar, LoginView
from .home import HomeView
from .theme import CustomComponents
from ..utilities.auth import AuthManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

THEME_PATH = Path("launcher_app/app/views/theme")


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------

@TrameApp()
class App:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.ctrl = self.server.controller
        binding = TrameBinding(self.server.state)
        self.home_vm, self.user_vm = create_viewmodels(binding)
        self.auth = AuthManager()
        self.css = None
        try:
            with open(THEME_PATH / "core_style.scss", "r") as scss_file:
                self.css = compile(string=scss_file.read())
        except Exception as e:
            logger.warning("Could not load base scss stylesheet.")
            logger.error(e)
        self.vuetify_config = None
        try:
            with open(
                THEME_PATH / "vuetify_config.json",
                "r"
            ) as vuetify_config:
                self.vuetify_config = json.load(vuetify_config)
        except Exception as e:
            logger.warning("Could not load vuetify config.")
            logger.error(e)

        self.create_ui()


    @property
    def state(self):
        return self.server.state

    def create_ui(self):
        self.state.trame__title = "Single Crystal Diffraction Dashboard"

        with SinglePageLayout(
            self.server,
            vuetify_config=self.vuetify_config
        ) as layout:
            client.Style(self.css)

            layout.title.set_text("Single Crystal Diffraction Dashboard")
            with layout.toolbar:
                LogoutToolbar(self.user_vm)
            with layout.content:
                with vuetify.VContainer(classes="align-start d-flex justify-center mt-8"):
                    LoginView(self.user_vm)
                    HomeView(self.state, self.server, self.home_vm)

            CustomComponents.Footer(layout)

            return layout
