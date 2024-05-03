import re
from functools import partial

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
        self.job_vm.job_state_bind.connect("job_state")
        self.job_vm.jobs_bind.connect("jobs")
        self.user_vm = user_view_model
        self.js_navigate = client.JSEval(
                exec="window.open($event,'_blank')"
        ).exec

        self.create_ui()

        self.job_vm.update_view()

    def create_ui(self):
        with vuetify.VRow(align="center"):
            vuetify.VBtn(
                "Start Topaz Reduction tool",
                id="start-topaz-btn",
                click=self.invoke_topaz_tool,
                style="padding: 10px; margin: 10px;",
            )
            vuetify.VProgressCircular(
                id="launch_tool_progress",
                color="red",
                indeterminate=True,
                v_show="job_state =='launching'"
            )
        with vuetify.VRow(align="center", v_for="(job_info, job) in jobs"):
            vuetify.VTextField(" Job ID: {{ job }}")
            vuetify.VTextField("{{ job_info.tool_id }}")
            vuetify.VBtn("Go to Tool", click=partial(self.navigate_to_topaz_tool, ""), style="margin: 10px;")
            vuetify.VBtn("Stop", click=partial(self.stop_topaz_job, ""), style="margin: 10px;")

    @asynchronous.task
    async def invoke_topaz_tool(self):
        current_url = await self.job_vm.start_job("neutrons_trame_topaz")
        if current_url is not None:
            self.js_navigate(current_url)

    def navigate_to_topaz_tool(self, job_url):
        for job, info in self.job_vm.jobs.items():
            if info["tool_id"] == "neutrons_trame_topaz":
                url = info["url"]
                self.js_navigate(url)

    @asynchronous.task
    async def stop_topaz_job(self, job_id):
        for job, info in self.job_vm.jobs.items():
            if info["tool_id"] == "neutrons_trame_topaz":
                await self.job_vm.stop_job(job)
                break
