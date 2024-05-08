from launcher_app.app.models.job import JobModel
from launcher_app.app.models.tool import ToolModel
from launcher_app.app.view_models.home import HomeViewModel




def create_viewmodels(binding):
    job_model = JobModel()
    tool_model = ToolModel()
    home_vm = HomeViewModel(job_model, tool_model, binding)
    return home_vm
