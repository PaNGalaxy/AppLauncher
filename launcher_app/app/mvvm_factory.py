from launcher_app.app.models.job import JobModel
from launcher_app.app.models.user import UserModel
from launcher_app.app.view_models.job import JobViewModel
from launcher_app.app.view_models.user import UserViewModel



def create_viewmodels(binding):
    job_model = JobModel()
    user_model = UserModel()
    job_vm = JobViewModel(job_model, binding)
    user_vm = UserViewModel(user_model, binding)
    return job_vm, user_vm
