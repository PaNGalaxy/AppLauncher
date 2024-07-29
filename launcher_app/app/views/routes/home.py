from trame_facade.components import EasyGrid

from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html as html


class HomeView:

    def __init__(self, server, view_model, vuetify_config):
        self.server = server
        self.ctrl = self.server.controller

        self.js_navigate = client.JSEval(exec="window.open($event,'_blank')").exec

        self.home_vm = view_model["home"]
        self.home_vm.galaxy_running_bind.connect("galaxy_running")
        self.home_vm.galaxy_url_bind.connect("galaxy_url")
        self.home_vm.job_state_bind.connect("job_state")
        self.home_vm.jobs_bind.connect("jobs")
        self.home_vm.tools_bind.connect("tools")
        self.home_vm.tool_list_bind.connect("tool_list")
        self.home_vm.logged_in_bind.connect("is_logged_in")
        self.home_vm.auto_open_bind.connect("auto_open")
        self.home_vm.navigation_bind.connect(self.js_navigate)

        self.user_vm = view_model["user"]
        self.user_vm.given_name_bind.connect("given_name")
        self.user_vm.email_bind.connect("email")
        self.user_vm.logged_in_bind.connect("is_logged_in")

        self.vuetify_config = vuetify_config

        self.create_ui()

        self.home_vm.update_view()
        self.home_vm.monitor_task.start_monitor()

    def create_ui(self):
        # This is painful but the only way I've found so far to handle this situation.
        # Basically, the idea is to check if the authentication status has changed since
        # the last page load, and if so, redirect the user to the last page they were on.
        client.ClientTriggers(
            mounted=(
                "window.localStorage.getItem('last_path') !== 'null' && "
                "window.localStorage.getItem('last_path') !== $route.path && "
                "is_logged_in && "
                "window.localStorage.getItem('logged_in') !== is_logged_in.toString() "
                " ? (window.localStorage.setItem('logged_in', is_logged_in),"
                "    $router.push(window.localStorage.getItem('last_path')))"
                " : (window.localStorage.setItem('logged_in', is_logged_in),"
                "    window.localStorage.setItem('last_path', null));"
            )
        )

        with vuetify.VContainer(classes="align-start d-flex justify-center mt-16"):
            with vuetify.VCard(width=1280):
                vuetify.VCardTitle(
                    "Welcome to the Neutrons App Dashboard", classes="text-center"
                )
                with vuetify.VCardText():
                    html.P(
                        (
                            "You can view the different categories of tools available below. "
                            "Simply click on a category to access its tools."
                        ),
                        classes="text-center",
                    )

                    with EasyGrid(cols_per_row=3):
                        for key, category in self.home_vm.tools.items():
                            vuetify.VCard(
                                append_icon="mdi-open-in-app",
                                classes="d-flex fill-height flex-column justify-center",
                                subtitle=category["description"],
                                title=category["name"],
                                to=f"/{key}",
                            )
