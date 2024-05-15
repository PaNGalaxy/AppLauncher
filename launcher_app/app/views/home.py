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
        self.home_vm.status_bind.connect("status")
        self.js_navigate = client.JSEval(
            exec="window.open($event,'_blank')"
        ).exec
        self.home_vm.navigation_bind.connect(self.js_navigate)
        self.create_ui()

        self.home_vm.update_view()

    def create_ui(self):
        with vuetify.VRow():
            vuetify.VTextField("{{ status }}")
        with vuetify.VRow(align="center", v_for="tool in tools"):
            vuetify.VBtn(
                "{{ tool.name }}",
                id="{{ tool.name }}-start-btn",
                click=(self.home_vm.start_job, "[tool.id]"),
                style="padding: 10px; margin: 10px;",
            )
        vuetify.VProgressCircular(
            id="launch_tool_progress",
            color="red",
            indeterminate=True,
            v_show="job_state =='launching'",
            style="margin-top: 10px;"
        )
        with vuetify.VList(shaped=True, classes="job_list_container", style="margin-top: 10px;"):
            with vuetify.VListItem(align="center", v_for="(job_info, job_id) in jobs", style="margin: 5px;"):
                vuetify.VTextField(" Job ID: {{ job_id }}")
                vuetify.VTextField("{{ job_info.tool_id }}")
                html.A("Go to Job", href=("job_info.url",), target="_blank")
                vuetify.VBtn("Stop", click=(self.home_vm.stop_job, "[job_id]"), style="margin: 10px;")
