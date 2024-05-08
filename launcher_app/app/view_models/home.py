import logging

from py_mvvm.interface import BindingInterface
from launcher_app.app.models.job import JobModel
from launcher_app.app.models.tool import ToolModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class HomeViewModel:

    def __init__(self, job_model: JobModel, tool_model: ToolModel, binding: BindingInterface):
        self.job_model = job_model
        self.job_state = None
        self.jobs = {}
        self.job_state_bind = binding.new_bind(self.job_state)
        self.jobs_bind = binding.new_bind(self.jobs)
        self.navigation_bind = binding.new_bind()
        self.tool_model = tool_model
        self.tool_list = None
        self.tool_list_bind = binding.new_bind()

    async def start_job(self, tool_id):
        if not self.job_state in ["launching", "launched"]:
            self.job_state = "launching"
            self.update_view()
            try:
                url, job_id = await self.job_model.galaxy.invoke_interactive_tool(tool_id)
                self.jobs[job_id] = {"tool_id": tool_id, "url": url}
                self.job_state = "launched"
            except Exception as e:
                self.job_state = None
                logger.error(e)
                url = None
            self.update_view()
            self.navigation_bind.update_in_view(url)
        else:
            logger.warning(f"Already {self.job_state} job.")
        return None

    async def stop_job(self, job_id):
        success = await self.job_model.galaxy.stop_job(job_id)
        if success:
            self.jobs.pop(job_id)
            self.job_state = None
        self.update_view()
        return success

    def update_view(self):
        self.job_state_bind.update_in_view(self.job_state)
        self.jobs_bind.update_in_view(self.jobs)
        self.tool_list = self.tool_model.get_tools()
        self.tool_list_bind.update_in_view(self.tool_list)
