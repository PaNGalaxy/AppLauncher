from functools import partial

from trame.app import asynchronous
from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html as html
from launcher_app.app.view_models.job import JobViewModel
from launcher_app.app.view_models.tool import ToolViewModel
from launcher_app.app.view_models.user import UserViewModel


class HomeView:

    def __init__(self, state, server, job_view_model: JobViewModel, user_view_model: UserViewModel, tool_view_model: ToolViewModel):
        self.state = state
        self.server = server
        self.ctrl = self.server.controller
        self.job_vm = job_view_model
        self.job_vm.job_state_bind.connect("job_state")
        self.job_vm.jobs_bind.connect("jobs")
        self.user_vm = user_view_model
        self.tool_vm = tool_view_model
        self.tool_vm.tool_list_bind.connect("tools")
        self.js_navigate = client.JSEval(
                exec="window.open($event,'_blank')"
        ).exec
        self.job_vm.navigation_bind.connect(self.js_navigate)
        self.create_ui()

        self.job_vm.update_view()

    def create_ui(self):
        for tool in self.tool_vm.get_tools():
            with vuetify.VRow(align="center"):
                vuetify.VBtn(
                    tool["name"],
                    id=f"{tool['name']}-start-btn",
                    click=partial(self.job_vm.start_job, tool["id"]),
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
                vuetify.VBtn("Stop", click=(self.job_vm.stop_job, "[job_id]"), style="margin: 10px;")
