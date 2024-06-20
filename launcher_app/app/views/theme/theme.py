import json
import logging
from pathlib import Path

import sass

from trame.app import get_server
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import client, vuetify3 as vuetify
from trame_client.widgets import html


THEME_PATH = Path(__file__).parent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ThemedApp:
    """Parent class for Trame applications that injects theming into the application."""

    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.css = None
        try:
            with open(THEME_PATH / "core_style.scss", "r") as scss_file:
                self.css = sass.compile(string=scss_file.read())
        except Exception as e:
            logger.warning("Could not load base scss stylesheet.")
            logger.error(e)
        self.vuetify_config = None
        try:
            with open(THEME_PATH / "vuetify_config.json", "r") as vuetify_config:
                self.vuetify_config = json.load(vuetify_config)
        except Exception as e:
            logger.warning("Could not load vuetify config.")
            logger.error(e)

    def create_ui(self):
        with VAppLayout(self.server, vuetify_config=self.vuetify_config) as layout:
            client.Style(self.css)

            with vuetify.VAppBar() as toolbar:
                layout.toolbar = toolbar

                vuetify.VAppBarTitle(
                    classes="cursor-pointer flex-0-1 py-2",
                    text=("trame__title",),
                    click="$router.push('/')",
                )
                vuetify.VSpacer()
                with html.Div(classes="mr-2") as actions:
                    layout.actions = actions

            layout.content = vuetify.VMain()

            with vuetify.VFooter(
                app=True, classes="my-0 py-0 text-center justify-center", border=True
            ) as footer:
                layout.footer = footer

                vuetify.VProgressCircular(
                    classes="ml-n3 mr-1",
                    color="primary",
                    indeterminate=("galaxy_running",),
                    size=16,
                    width=3,
                )
                html.A(
                    "Powered by Calvera",
                    classes="text-grey-lighten-1 text-caption text-decoration-none",
                    href=("galaxyLink",),
                    target="_blank",
                )
                vuetify.VSpacer()
                footer.add_child(
                    '<a href="https://www.ornl.gov/" class="text-grey-lighten-1 text-caption text-decoration-none" '
                    'target="_blank">© 2024 ORNL</a>'
                )

            return layout
