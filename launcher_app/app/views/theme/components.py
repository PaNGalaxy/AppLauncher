import json
import logging
from pathlib import Path
from uuid import uuid4

import sass
from trame.app import get_server
from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame_client.widgets import html

from launcher_app.app.views.base import SinglePageLayout


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

THEME_PATH = Path("launcher_app/app/views/theme")


class ThemedApp:
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
            with open(
                THEME_PATH / "vuetify_config.json",
                "r"
            ) as vuetify_config:
                self.vuetify_config = json.load(vuetify_config)
        except Exception as e:
            logger.warning("Could not load vuetify config.")
            logger.error(e)

    @property
    def state(self):
        return self.server.state

    def create_ui(self):
        with SinglePageLayout(
            self.server,
            vuetify_config=self.vuetify_config
        ) as layout:
            client.Style(self.css)

            with layout.footer as footer:
                vuetify.VProgressCircular(
                    classes="ml-n3 mr-1",
                    color="primary",
                    indeterminate=("!!galaxy_running",),
                    size=16,
                    width=3,
                ),
                html.A(
                    "Powered by Calvera",
                    classes="text-grey-lighten-1 text-caption text-decoration-none",
                    href=("galaxyLink",),
                    target="_blank")
                vuetify.VSpacer()
                footer.add_child(
                    '<a href="https://www.ornl.gov/" class="text-grey-lighten-1 text-caption text-decoration-none" '
                    'target="_blank">© 2024 ORNL</a>'
                )

            return layout


class CustomComponents:
    def List(server, items, action=None, header=None):
        # If a user creates multiple lists, we need a way to inject the list data into the front-end
        # without collisions. This is my approach to handling the situation.
        with server.state:
            if server.state.theme is None:
                server.state.theme = {}
            if "list_items" not in server.state.theme:
                server.state.theme["list_items"] = {}
            key = str(uuid4()).replace('-', '_')
            server.state.theme["list_items"][key] = items

        with vuetify.VList():
            if header is not None:
                vuetify.VListSubheader(header)
            with html.Div(classes="border-thin"):
                with vuetify.VListItem(
                    v_for=(f"(item, index) in theme.list_items.{key}",),
                    classes="pa-2"
                ) as list_item:
                    vuetify.VListItemTitle("{{ item.title }}")
                    vuetify.VListItemSubtitle("{{ item.subtitle }}")

                    with vuetify.Template(v_slot_append=True, v_if=action is not None):
                        with vuetify.VListItemAction():
                            if callable(action):
                                action()