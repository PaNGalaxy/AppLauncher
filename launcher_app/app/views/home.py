from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html as html
from launcher_app.app.view_models.home import HomeViewModel
from launcher_app.app.views.theme import CustomComponents


class HomeView:

    def __init__(self, state, server, home_view_model: HomeViewModel):
        self.state = state
        self.server = server
        self.ctrl = self.server.controller
        self.home_vm = home_view_model
        self.home_vm.job_state_bind.connect("job_state")
        self.home_vm.jobs_bind.connect("jobs")
        self.home_vm.tool_list_bind.connect("tools")
        self.home_vm.logged_in_bind.connect("is_logged_in")
        self.js_navigate = client.JSEval(
            exec="window.open($event,'_blank')"
        ).exec
        self.home_vm.navigation_bind.connect(self.js_navigate)
        self.create_ui()
        self.home_vm.update_view()
        self.home_vm.monitor_task.start_monitor()

    def _job_actions(self):
        with vuetify.VBtn(
            "Launch",
            v_if=("!['launched', 'launching'].includes(job_state[tools[index].id])",),
            click=(self.home_vm.start_job, "[tools[index].id]"),
            color="primary"
        ):
            vuetify.VIcon(icon="mdi-play")
        with vuetify.VBtn(
            "Open",
            v_if=("jobs[tools[index].id]",),
            click=(self.js_navigate, "[jobs[tools[index].id].url]"),
            color="primary"
        ):
            vuetify.VIcon(icon="mdi-open-in-new")
        with vuetify.VBtn(
            "Stop",
            v_if=("job_state[tools[index].id] === 'launched'",),
            click=(self.home_vm.stop_job, "[tools[index].id]"),
            color="error"
        ):
            vuetify.VIcon(icon="mdi-stop")
        vuetify.VProgressCircular(v_if=("job_state[tools[index].id] === 'launching'",))

    def create_ui(self):
        with vuetify.VCard(v_if="is_logged_in", width=800):
            CustomComponents.List(v_for="(tool, index) in tools", action=self._job_actions, header="Available Tools", subtitle=("tool.description",), title=("tool.name",))
