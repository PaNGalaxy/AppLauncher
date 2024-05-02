import logging

from py_mvvm.interface import BindingInterface
from launcher_app.app.models.job import JobModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class JobViewModel:

    def __init__(self, model: JobModel, binding: BindingInterface):
        self.model = model
        self.job_state = None
        self.job_state_bind = binding.new_bind(self.job_state)

    async def start_job(self, tool_id):
        if not self.job_state in ["launching", "launched"]:
            self.job_state = "launching"
            self.update_view()
            try:
                url = await self.model.galaxy.invoke_interactive_tool(tool_id)
                self.job_state = "launched"
            except Exception as e:
                self.job_state = None
                logger.error(e)
            self.update_view()
            return url
        else:
            logger.warning(f"Already {self.job_state} job.")
        return None

    def update_view(self):
        self.job_state_bind.update_in_view(self.job_state)
