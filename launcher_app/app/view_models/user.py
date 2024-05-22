from launcher_app.app.models.user import UserModel
from py_mvvm.interface import BindingInterface
from launcher_app.app.utilities.auth import TrameAuth as auth

class UserViewModel:

    def __init__(self, user: UserModel, binding: BindingInterface):
        self.user_model = user
        self.auth_url = user.get_auth_url()
        self.username = None
        self.email = None
        self.logged_in = None
        self.username_bind = binding.new_bind(self.username)
        self.email_bind = binding.new_bind(self.email)
        self.logged_in_bind = binding.new_bind(self.logged_in)
        auth.register_auth_listner(self.update_view)

    def get_auth_url(self):
        return self.user_model.get_auth_url()

    def update_view(self):
        self.username = self.user_model.get_username()
        self.username_bind.update_in_view(self.username)
        self.email = self.user_model.get_email()
        self.email_bind.update_in_view(self.email)
        self.logged_in = self.user_model.logged_in()
        self.logged_in_bind.update_in_view(self.logged_in)






