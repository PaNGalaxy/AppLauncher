from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html as html
from launcher_app.app.view_models.home import HomeViewModel


class HomeView:

    def __init__(self, server, view_model):
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

        self.user_vm = view_model["user"]
        self.user_vm.given_name_bind.connect("given_name")
        self.user_vm.email_bind.connect("email")
        self.user_vm.logged_in_bind.connect("is_logged_in")

        self.create_ui()

        self.home_vm.update_view()
        self.home_vm.monitor_task.start_monitor()

    def create_ui(self):
        # This is painful but the only way I've found so far to handle this situation.
        # Basically, the idea is to check if the authentication status has changed since
        # the last page load, and if so, redirect the user to the last page they were on.
        client.ClientTriggers(
            mounted=(
                "window.localStorage.getItem('lastPath') !== 'null' && "
                "window.localStorage.getItem('lastPath') !== $route.path && "
                "is_logged_in && "
                "window.localStorage.getItem('loggedIn') !== is_logged_in.toString() "
                " ? (window.localStorage.setItem('loggedIn', is_logged_in),"
                "    $router.push(window.localStorage.getItem('lastPath')))"
                " : (window.localStorage.setItem('loggedIn', is_logged_in),"
                "    window.localStorage.setItem('lastPath', null));"
            )
        )

        with vuetify.VContainer(classes="align-start d-flex justify-center mt-8"):
            with vuetify.VCard(width=800):
                vuetify.VCardTitle(
                    "Welcome to the Neutrons App Dashboard", classes="text-center"
                )
                with vuetify.VCardText():
                    html.P(
                        "You can view the different categories of tools available below."
                        "To see the tools available for a category, simply click on it to"
                        "view the available tools."
                    )

                    with vuetify.VList():
                        for key in self.home_vm.tools:
                            category = self.home_vm.tools[key]

                            with vuetify.VListItem(
                                classes="my-4 pa-4", to=f"/category/{key}"
                            ):
                                vuetify.VListItemTitle(category["name"])
                                vuetify.VListItemSubtitle(category["description"])
