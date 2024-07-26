from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html as html


class CategoryView:

    def __init__(self, server, view_model):
        self.server = server
        self.ctrl = self.server.controller

        self.js_local_storage = client.JSEval(
            exec="window.localStorage.setItem($event.key, $event.value)"
        ).exec
        self.js_navigate = client.JSEval(exec="window.open($event,'_blank')").exec

        self.home_vm = view_model["home"]
        self.home_vm.galaxy_running_bind.connect("galaxy_running")
        self.home_vm.galaxy_url_bind.connect("galaxy_url")
        self.home_vm.job_state_bind.connect("job_state")
        self.home_vm.jobs_bind.connect("jobs")
        self.home_vm.tool_list_bind.connect("tools")
        self.home_vm.tool_list_bind.connect("tool_list")
        self.home_vm.logged_in_bind.connect("is_logged_in")
        self.home_vm.auto_open_bind.connect("auto_open")
        self.home_vm.local_storage_bind.connect(self.js_local_storage)
        self.home_vm.navigation_bind.connect(self.js_navigate)

        self.user_vm = view_model["user"]
        self.user_vm.given_name_bind.connect("given_name")
        self.user_vm.email_bind.connect("email")
        self.user_vm.logged_in_bind.connect("is_logged_in")

        self.create_ui()

        self.home_vm.update_view()
        self.home_vm.monitor_task.start_monitor()

    def create_ui(self):
        client.ClientTriggers(
            mounted=(
                self.home_vm.set_local_storage,
                (
                    "[{"
                    "  'auto_open': window.localStorage.getItem('auto_open') === 'true',"
                    "  'last_path': $route.path,"
                    "  'logged_in': is_logged_in"
                    "}]"
                ),
            )
        )

        with vuetify.VBreadcrumbs(classes="position-fixed", style={"top": "64px"}):
            with vuetify.VBreadcrumbsItem(to="/"):
                html.Span("Home")
            vuetify.VBreadcrumbsDivider()
            with vuetify.VBreadcrumbsItem():
                html.Span("{{ tools[$route.params.category]['name'] }}")

        with vuetify.VContainer(classes="align-start d-flex justify-center mt-16"):
            with vuetify.VCard(width=800):
                vuetify.VCardTitle(
                    "{{ tools[$route.params.category]['name'] }} Applications",
                    classes="text-center",
                )
                vuetify.VCardSubtitle(
                    (
                        "The below tools are currently supported for running on Calvera. "
                        "You must be signed in to launch them. "
                        "You may sign in using the button in the top right corner of this page."
                    )
                )
                with vuetify.VCardText():
                    with vuetify.VList():
                        vuetify.VListSubheader(
                            "Available Tools",
                            v_if=("tools[$route.params.category]['tools'].length > 0",),
                        )
                        vuetify.VListSubheader(
                            "Stay tuned, we will be adding tools here soon!",
                            v_else=True,
                            classes="justify-center",
                        )
                        with vuetify.VListItem(
                            v_for=(
                                "(tool, index) in tools[$route.params.category]['tools']"
                            ),
                            classes="pa-2",
                        ):
                            vuetify.VListItemTitle("{{ tool['name'] }}")
                            vuetify.VListItemSubtitle("{{ tool['description'] }}")
                            with vuetify.Template(v_slot_append=True):
                                with vuetify.VListItemAction():
                                    with html.Div(v_if="!is_logged_in"):
                                        vuetify.VBtn(
                                            "Sign in to run apps",
                                            disabled=True,
                                        )
                                    with html.Div(v_else=True):
                                        with vuetify.VBtn(
                                            "Launch",
                                            v_if=(
                                                f"!['launched', 'launching', 'stopping'].includes(job_state[tool.id])",
                                            ),
                                            click=(self.home_vm.start_job, "[tool.id]"),
                                        ):
                                            vuetify.VIcon(icon="mdi-play")
                                        with vuetify.VBtn(
                                            "Open",
                                            v_if=("job_state[tool.id] === 'launched'",),
                                            click=(
                                                self.js_navigate,
                                                "[jobs[tool.id].url]",
                                            ),
                                        ):
                                            vuetify.VIcon(icon="mdi-open-in-new")
                                        with vuetify.VBtn(
                                            "Stop",
                                            v_if=("job_state[tool.id] === 'launched'",),
                                            click=(self.home_vm.stop_job, "[tool.id]"),
                                            color="error",
                                        ):
                                            vuetify.VIcon(icon="mdi-stop")
                                        vuetify.VProgressCircular(
                                            v_if=(
                                                "['launching', 'stopping'].includes(job_state[tool.id])",
                                            ),
                                            indeterminate=True,
                                        )
