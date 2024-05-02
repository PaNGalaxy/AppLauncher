from py_mvvm.interface import BindingInterface
from launcher_app.app.models.user import UserModel


class UserViewModel:
    def __init__(self, model: UserModel, binding: BindingInterface):
        self.model = model
