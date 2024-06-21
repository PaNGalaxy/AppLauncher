import argparse
import logging
import os
import threading

from trame.app import get_server
from trame.decorators import TrameApp
from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame_client.widgets import html

from .base import SinglePageLayout
from .model import Model
from .ui_config_panel import ConfigPanel
from .ui_execution_panel import ExecutionPanel
from .utilities import galaxy

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

GALAXY_UPDATE_INTERVAL_SEC = 10


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


@TrameApp()
class App:
    def _sync_histories(self):
        try:
            self.state.items_galaxyHistory = galaxy.get_histories(self.state)
            if self.state.galaxyHistory not in self.state.items_galaxyHistory:
                self.state.galaxyHistory = self.state.items_galaxyHistory[0]
        except:
            self.state.galaxyHistory = None
            self.state.items_galaxyHistory = []
        thread = threading.Timer(GALAXY_UPDATE_INTERVAL_SEC, self._sync_histories)
        thread.daemon = True
        thread.start()

    def _connect_to_galaxy(self, args):
        self.state.galaxyURL = args.galaxy_url or os.getenv("GALAXY_URL")
        self.state.galaxyLink = self.state.galaxyURL
        self.state.galaxyAPIKey = args.galaxy_key or os.getenv("GALAXY_API_KEY")
        initial_history = args.galaxy_history_id or os.getenv("GALAXY_HISTORY_ID")

        self._sync_histories()
        for history in self.state.items_galaxyHistory:
            if history["id"] == initial_history:
                self.state.galaxyHistory = history
                break
        if len(self.state.items_galaxyHistory) > 0 and not self.state.galaxyHistory:
            self.state.galaxyHistory = self.state.items_galaxyHistory[0]

    def __init__(self, server=None, data=None):
        self.server = get_server(server, client_type="vue3")

        # CLI
        self.server.cli.add_argument("--galaxy-url", help="URL of the Galaxy server")
        self.server.cli.add_argument("--galaxy-key", help="API key for accessing the Galaxy server")
        self.server.cli.add_argument("--galaxy-history-id", help="Default Galaxy history ID to use")
        self.server.cli.add_argument("--config", help="Path to configuration file")
        self.server.cli.add_argument("--session", help="Session identifier")
        args, _ = self.server.cli.parse_known_args()

        # TODO use it in auth
        root_path = os.environ.get("EP_PATH", "")
        # I don't think you need it in the state
        self.state.base_url = f"{root_path}/api/{args.session}/"
        print(f"Base URL to use: {self.state.base_url}")

        # todo:  can we put config as state variable so that a change to a nested field would trigger state change
        self.state.model = Model()
        self.state.config_file = None

        self._connect_to_galaxy(args)
        if args.config:
            self.state.model.loadConfig(open(args.config).read())
        self.state.error_dialog = False
        self.state.error_dialog_message = None
        self.update_ui()

    @property
    def state(self):
        return self.server.state

    def update_ui(self):
        with SinglePageLayout(self.server) as layout:
            client.Style(".v-label { opacity: 100; }")

            layout.title.set_text("Template Trame Application")

            with layout.content:
                ConfigPanel()
                ExecutionPanel()
                with vuetify.VDialog(
                        v_model="error_dialog",
                        width="auto"
                ):
                    with vuetify.VCard(classes="text-center", text=("error_dialog_message",)):
                        with vuetify.VCardActions():
                            vuetify.VBtn("Close", block=True, click="error_dialog = False", size="small",
                                         color="primary")
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
                    '<a href="https://www.ornl.gov/" class="text-grey-lighten-1 text-caption text-decoration-none" target="_blank">© 2024 ORNL</a>'
                )

            return layout
