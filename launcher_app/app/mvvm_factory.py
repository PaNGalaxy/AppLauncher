from launcher_app.app.models.job import JobModel
from launcher_app.app.models.tool import ToolModel
from launcher_app.app.models.user import UserModel
from launcher_app.app.view_models.home import HomeViewModel
from launcher_app.app.view_models.user import UserViewModel


def create_viewmodels(binding):
    job_model = JobModel()
    tool_model = ToolModel()
    user_model = UserModel()

    vm = {}
    vm["home"] = HomeViewModel(job_model, tool_model, user_model, binding)
    vm["user"] = UserViewModel(user_model, binding)

    return vm
