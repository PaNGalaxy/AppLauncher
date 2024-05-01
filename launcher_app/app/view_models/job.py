import logging

from py_mvvm.interface import BindingInterface
from launcher_app.app.models.job import JobModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class JobViewModel:

    def __init__(self, model: JobModel, binding: BindingInterface):
        self.model = model
        self.launching_job = False
        self.launching_job_bind = binding.new_bind(self.launching_job)

    async def start_job(self, tool_id):
        if not self.launching_job:
            self.launching_job = True
            self.update_view()
            try:
                url = await self.model.galaxy.invoke_interactive_tool(tool_id)
                return url
            except Exception as e:
                logger.error(e)
            self.launching_job = False
            self.update_view()
        else:
            logger.warning("Already launching job. Please wait.")
        return None

    def update_view(self):
        self.launching_job_bind.update_in_view(self.launching_job)
