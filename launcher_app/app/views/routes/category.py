from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html as html


class CategoryView:

    def __init__(self, server, view_model):
        self.server = server
        self.ctrl = self.server.controller

        self.js_navigate = client.JSEval(exec="window.open($event,'_blank')").exec

        self.home_vm = view_model["home"]
        self.home_vm.job_state_bind.connect("job_state")
        self.home_vm.jobs_bind.connect("jobs")
        self.home_vm.tool_list_bind.connect("tools")
        self.home_vm.tool_list_bind.connect("tool_list")
        self.home_vm.logged_in_bind.connect("is_logged_in")
        self.home_vm.navigation_bind.connect(self.js_navigate)

        self.create_ui()

        self.home_vm.update_view()
        self.home_vm.monitor_task.start_monitor()

    def create_ui(self):
        with vuetify.VBreadcrumbs():
            with vuetify.VBreadcrumbsItem(to="/"):
                html.Span("Home")
            vuetify.VBreadcrumbsDivider()
            with vuetify.VBreadcrumbsItem():
                html.Span("{{ tools[$route.params.category]['name'] }}")

        with vuetify.VContainer(classes="align-start d-flex justify-center mt-8"):
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
                    ),
                    classes="mb-4",
                )
                vuetify.VCardSubtitle(
                    "If you're interested in adding a tool, then please see our developer guide { link } "
                    "or contact { email } for more information.",
                )
                with vuetify.VCardText():
                    with vuetify.VList():
                        vuetify.VListSubheader(
                            "Available Tools",
                            v_if=("tools[$route.params.category]['tools'].length > 0",),
                        )
                        vuetify.VListSubheader(
                            "No Tools Available", v_else=True, classes="justify-center"
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
                                    with vuetify.VBtn(
                                        "Launch",
                                        v_if=(
                                            f"!['launched', 'launching'].includes(job_state[tool.id])",
                                        ),
                                        click=(self.home_vm.start_job, "[tool.id]"),
                                        color="secondary",
                                    ):
                                        vuetify.VIcon(icon="mdi-play")
                                    with vuetify.VBtn(
                                        "Open",
                                        v_if=("jobs[tool.id]",),
                                        click=(self.js_navigate, "[jobs[tool.id].url]"),
                                        color="secondary",
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
                                        v_if=("job_state[tool.id] === 'launching'",)
                                    )
