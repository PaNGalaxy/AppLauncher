from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html as html
from launcher_app.app.view_models.home import HomeViewModel

class HomeView:

    def __init__(self, state, server, home_view_model: HomeViewModel):
        self.state = state
        self.server = server
        self.ctrl = self.server.controller
        self.home_vm = home_view_model
        self.home_vm.job_state_bind.connect("job_state")
        self.home_vm.jobs_bind.connect("jobs")
        self.home_vm.tool_list_bind.connect("tools")
        self.js_navigate = client.JSEval(
            exec="window.open($event,'_blank')"
        ).exec
        self.home_vm.navigation_bind.connect(self.js_navigate)
        self.create_ui()

        self.home_vm.update_view()

    def create_ui(self):
        html.H2("Dashboard", classes="view-header-label", style="margin-bottom: 1em;")
        with vuetify.VTabs(
                v_model=("active_tab", 0),
                bg_color="lightgray",
                slider_color="red"
        ):
            vuetify.VTab("{{tool.name}}", classes="tool-btn", selected_class="tool-btn-selected", v_for="tool in tools")
        with vuetify.VCard(id="home-view-container", style="margin: auto; padding: 20px; width: 100%; height: 100%;"):
            with vuetify.VContainer(fluid=True):
                with vuetify.VWindow(v_model="active_tab"):
                    with vuetify.VWindowItem(value=1, reverse_transition="false", transition="false"):
                        html.P("This is where you will launch the Garnet application. The UI is a work in progress.")
                        vuetify.VProgressCircular(color="red", classes="tool-progress-bar", indeterminate=True,
                                                  v_show="job_state[tools[active_tab].id] == 'launching'",
                                                  style="margin-top: 1em")
                        with vuetify.VRow(align="center", classes="control-btn-group", style="margin-top: 10em; margin-left: 1em;"):
                            with vuetify.VCol(classes="pa-4"):
                                vuetify.VBtn(
                                    "Launch",
                                    click=(self.home_vm.start_job, "[tools[active_tab].id]"),
                                    classes="control-btn",
                                    disabled=("job_state[tools[active_tab].id] == 'launched'",),
                                    style="margin-right: 1em;"
                                )
                                vuetify.VBtn("Stop Tool", classes="control-btn",
                                             click=(self.home_vm.stop_job, "[tools[active_tab].id]"),
                                             disabled=("job_state[tools[active_tab].id] != 'launched'",),
                                             style="margin-right: 1em;")
                                vuetify.VBtn("Navigate to Tool", classes="control-btn",
                                             click=(self.js_navigate, "[jobs[tools[active_tab].id].url]"),
                                             disabled=("job_state[tools[active_tab].id] != 'launched'",),
                                             style="margin-right: 1em;")
                    with vuetify.VWindowItem(value=2, reverse_transition="false", transition="false"):
                        html.P("This is where you will launch the Topaz application. The UI is a work in progress.")
                        vuetify.VProgressCircular(color="red", classes="tool-progress-bar", indeterminate=True,
                                                  v_show="job_state[tools[active_tab].id] == 'launching'",
                                                  style="margin-top: 1em")
                        with vuetify.VRow(align="center", classes="control-btn-group", style="margin-top: 10em; margin-left: 1em;"):
                            with vuetify.VCol(classes="pa-4"):
                                vuetify.VBtn(
                                    "Launch",
                                    click=(self.home_vm.start_job, "[tools[active_tab].id]"),
                                    classes="control-btn",
                                    disabled=("job_state[tools[active_tab].id] == 'launched'",),
                                    style="margin-right: 1em;"
                                )
                                vuetify.VBtn("Stop Tool", classes="control-btn",
                                             click=(self.home_vm.stop_job, "[tools[active_tab].id]"),
                                             disabled=("job_state[tools[active_tab].id] != 'launched'",),
                                             style="margin-right: 1em;"
                                             )
                                vuetify.VBtn("Navigate to Tool", classes="control-btn",
                                             click=(self.js_navigate, "[jobs[tools[active_tab].id].url]"),
                                             disabled=("job_state[tools[active_tab].id] != 'launched'",),
                                             style="margin-right: 1em;"
                                             )
