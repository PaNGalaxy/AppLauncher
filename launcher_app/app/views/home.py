from trame.app import asynchronous
from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from launcher_app.app.view_models.job import JobViewModel
from launcher_app.app.view_models.user import UserViewModel


class HomeView:

    def __init__(self, state, server, job_view_model: JobViewModel, user_view_model: UserViewModel):
        self.state = state
        self.server = server
        self.ctrl = self.server.controller
        self.job_vm = job_view_model
        self.job_vm.launching_job_bind.connect("job_launching")
        self.user_vm = user_view_model
        self.js_navigate = client.JSEval(
                exec="window.location.href = $event"
        ).exec

        self.create_ui()

        self.job_vm.update_view()

    def create_ui(self):
        with vuetify.VRow(align="center"):
            vuetify.VBtn("Start Topaz Reduction tool", id="login-button-xcams", click=self.invoke_topaz_tool, style="padding: 10px; margin: 10px;")
            vuetify.VProgressCircular(id="launch_tool_progress", color="red", indeterminate=True, v_show="job_launching")

    @asynchronous.task
    async def invoke_topaz_tool(self):
        current_url = await self.job_vm.start_job("neutrons_trame_topaz")
        if current_url is not None:
            self.js_navigate(current_url)

