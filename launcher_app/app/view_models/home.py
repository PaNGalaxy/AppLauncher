import logging

from py_mvvm.interface import BindingInterface
from launcher_app.app.models.job import JobModel
from launcher_app.app.models.tool import ToolModel
from launcher_app.app.models.user import UserModel
from launcher_app.app.utilities.monitor import TaskMonitor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_MONITOR_UPDATE_FREQUENCY = 1


class HomeViewModel:

    def __init__(
        self,
        job_model: JobModel,
        tool_model: ToolModel,
        user_model: UserModel,
        binding: BindingInterface,
    ):
        self.job_model = job_model
        self.tool_model = tool_model
        self.user_model = user_model

        self.job_state = {}
        self.jobs = {}
        self.galaxy_jobs = 0
        self.galaxy_running_bind = binding.new_bind()
        self.galaxy_url_bind = binding.new_bind()
        self.job_state_bind = binding.new_bind(self.job_state)
        self.jobs_bind = binding.new_bind(self.jobs)
        self.navigation_bind = binding.new_bind()
        self.tools_bind = binding.new_bind()
        self.tool_list_bind = binding.new_bind()
        self.monitor_task = TaskMonitor(self.monitor, DEFAULT_MONITOR_UPDATE_FREQUENCY)
        self.tools = self.tool_model.get_tools()
        self.tool_list = self.tool_model.get_tools(as_list=True)
        self.auto_open_tool_list = []
        for tool in self.tool_list:
            self.job_state[tool["id"]] = None

        self.logged_in = None
        self.logged_in_bind = binding.new_bind(self.logged_in)
        self.user_model.auth.register_auth_listener(self.update_view)

    async def start_job(self, tool_id):
        if not self.check_tool_limit(tool_id):
            # TODO: maybe set some status here
            self.update_view()
            return

        self.galaxy_jobs += 1
        self.job_state[tool_id] = "launching"
        self.update_view()

        await self.job_model.galaxy.invoke_interactive_tool(tool_id)
        self.auto_open_tool_list.append(tool_id)

    async def stop_job(self, tool_id):
        self.galaxy_jobs += 1
        self.job_state[tool_id] = "stopping"
        self.update_view()

        success = await self.job_model.galaxy.stop_job(self.jobs[tool_id]["job_id"])

        self.galaxy_jobs -= 1
        self.update_view()

        return success

    def check_tool_limit(self, tool_id):
        if tool_id in self.jobs.keys() or self.job_state[tool_id]:
            return False
        return True

    def monitor(self):
        running_tools = self.job_model.galaxy.check_running_tools()
        for tool in self.tool_list:
            try:
                matched_tool = next(
                    filter(lambda x: x["tool_id"] == tool["id"], running_tools)
                )
                self.jobs[tool["id"]] = {
                    "job_id": matched_tool["job_id"],
                    "url": matched_tool["url"],
                }
                if matched_tool["state"] == "running":
                    if self.job_state[tool["id"]] == "launching":
                        self.galaxy_jobs -= 1
                    if self.job_state[tool["id"]] != "stopping":
                        self.job_state[tool["id"]] = "launched"
            except StopIteration:
                if self.job_state[tool["id"]] not in ["launching"]:
                    self.job_state[tool["id"]] = None
                if self.jobs.get(tool["id"], None):
                    self.jobs.pop(tool["id"])
        if len(self.auto_open_tool_list) > 0:
            for t in self.auto_open_tool_list.copy():
                if self.jobs[t]["url"]:
                    self.navigation_bind.update_in_view(self.jobs[t]["url"])
                    self.auto_open_tool_list.remove(t)

        self.update_view()

    def update_view(self):
        self.galaxy_running_bind.update_in_view(self.galaxy_jobs > 0)
        self.galaxy_url_bind.update_in_view(self.job_model.galaxy.galaxy_url)
        self.jobs_bind.update_in_view(self.jobs)
        self.tools = self.tool_model.get_tools()
        self.tool_list = self.tool_model.get_tools(as_list=True)
        self.tools_bind.update_in_view(self.tools)
        self.tool_list_bind.update_in_view(self.tool_list)
        self.job_state_bind.update_in_view(self.job_state)
        self.logged_in = self.user_model.logged_in()
        self.logged_in_bind.update_in_view(self.logged_in)
