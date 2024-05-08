from launcher_app.app.models.job import JobModel
from launcher_app.app.models.tool import ToolModel
from launcher_app.app.models.user import UserModel
from launcher_app.app.view_models.job import JobViewModel
from launcher_app.app.view_models.tool import ToolViewModel
from launcher_app.app.view_models.user import UserViewModel



def create_viewmodels(binding):
    job_model = JobModel()
    user_model = UserModel()
    tool_model = ToolModel()
    job_vm = JobViewModel(job_model, binding)
    user_vm = UserViewModel(user_model, binding)
    tool_vm = ToolViewModel(tool_model, binding)
    return job_vm, user_vm, tool_vm
