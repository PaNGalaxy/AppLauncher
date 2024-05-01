import logging

from py_mvvm.trame_binding import TrameBinding

from trame.app import get_server
from trame.decorators import TrameApp
from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame_client.widgets import html

from launcher_app.app.mvvm_factory import create_viewmodels
from launcher_app.app.views.base import SinglePageLayout
from .login import LoginView
from .home import HomeView

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CSS_PATH = "launcher_app/app/views/styles/core_style.css"


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------

@TrameApp()
class App:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.ctrl = self.server.controller
        binding = TrameBinding(self.server.state)
        self.job_vm, self.user_vm = create_viewmodels(binding)
        self.css = None
        try:
            with open(CSS_PATH, "r") as css_sheet:
                self.css = css_sheet.read()
        except Exception as e:
            logger.warning("Could not load base css stylesheet.")
            logger.error(e)

        self.create_ui()

    @property
    def state(self):
        return self.server.state


    def create_ui(self):
        
        with SinglePageLayout(self.server) as layout:
            client.Style(self.css)

            layout.title.set_text("Trame App Launcher")
            with layout.content:
                with vuetify.VContainer():

                    # LoginView()
                    HomeView(self.state, self.server, self.job_vm, self.user_vm)
                                     
            with layout.footer as footer:
                vuetify.VProgressCircular(
                    indeterminate=("!!galaxy_running",),
                    color="#04a94d",
                    size=16,
                    width=3,
                    classes="ml-n3 mr-1",
                ),
                html.A("Powered by Calvera", href=("galaxyLink",),
                       classes="text-grey-lighten-1 text-caption text-decoration-none", target="_blank")
                vuetify.VSpacer()
                footer.add_child(
                    '<a href="https://www.ornl.gov/" class="text-grey-lighten-1 text-caption text-decoration-none" '
                    'target="_blank">© 2024 ORNL</a>'
                )

            return layout
