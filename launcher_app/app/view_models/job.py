import logging

from py_mvvm.interface import BindingInterface
from launcher_app.app.models.job import JobModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class JobViewModel:

    def __init__(self, model: JobModel, binding: BindingInterface):
        self.model = model
        self.job_state = None
        self.jobs = {}
        self.job_state_bind = binding.new_bind(self.job_state)
        self.jobs_bind = binding.new_bind(self.jobs)

    async def start_job(self, tool_id):
        if not self.job_state in ["launching", "launched"]:
            self.job_state = "launching"
            self.update_view()
            try:
                url, job_id = await self.model.galaxy.invoke_interactive_tool(tool_id)
                self.jobs[job_id] = {"tool_id": tool_id, "url": url}
                self.job_state = "launched"
            except Exception as e:
                self.job_state = None
                logger.error(e)
                url = None
            self.update_view()
            return url
        else:
            logger.warning(f"Already {self.job_state} job.")
        return None

    async def stop_job(self, job_id):
        success = await self.model.galaxy.stop_job(job_id)
        if success:
            self.jobs.pop(job_id)
            self.job_state = None
        self.update_view()
        return success

    def update_view(self):
        self.job_state_bind.update_in_view(self.job_state)
        self.jobs_bind.update_in_view(self.jobs)
