from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html as html

from launcher_app.app.views.theme.components import EasyGrid


class HomeView:

    def __init__(self, server, view_model, vuetify_config):
        self.server = server
        self.ctrl = self.server.controller

        self.js_navigate = client.JSEval(exec="window.open($event,'_blank')").exec

        self.home_vm = view_model["home"]
        self.home_vm.job_state_bind.connect("job_state")
        self.home_vm.jobs_bind.connect("jobs")
        self.home_vm.tools_bind.connect("tools")
        self.home_vm.tool_list_bind.connect("tool_list")
        self.home_vm.logged_in_bind.connect("is_logged_in")
        self.home_vm.navigation_bind.connect(self.js_navigate)

        self.vuetify_config = vuetify_config

        self.create_ui()

        self.home_vm.update_view()
        self.home_vm.monitor_task.start_monitor()

    def create_ui(self):
        with vuetify.VContainer(classes="align-start d-flex justify-center mt-16"):
            with vuetify.VCard(width=800):
                vuetify.VCardTitle(
                    "Welcome to the Neutrons App Dashboard", classes="text-center"
                )
                with vuetify.VCardText():
                    html.P(
                        "You can view the different categories of tools available below. "
                        "To see the tools available for a category, simply click on it."
                    )

                    with EasyGrid(cols_per_row=2):
                        for key, category in self.home_vm.tools.items():
                            color = (
                                self.vuetify_config["theme"]["themes"]
                                .get(category["theme"], {})
                                .get("colors", {})
                                .get("primary", "#000000")
                            )

                            vuetify.VCard(
                                append_icon="mdi-open-in-app",
                                flat=True,
                                prepend_icon=category["icon"],
                                style={
                                    "background-color": f"{color}19",  # 8-digit hex code, 19 represents ~10% opacity
                                    "border-color": color,
                                    "border-width": "1px",
                                },
                                subtitle=category["description"],
                                title=category["name"],
                                to=f"/category/{key}",
                            )
