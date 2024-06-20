from launcher_app.app.models.user import UserModel
from py_mvvm.interface import BindingInterface


class UserViewModel:

    def __init__(self, user: UserModel, binding: BindingInterface):
        self.user_model = user
        self.username = None
        self.email = None
        self.logged_in = None
        self.given_name_bind = binding.new_bind(self.username)
        self.email_bind = binding.new_bind(self.email)
        self.logged_in_bind = binding.new_bind(self.logged_in)
        self.user_model.auth.register_auth_listener(self.update_view)

    def get_auth_url(self):
        return self.user_model.auth.get_ucams_auth_url()

    def get_xcams_auth_url(self):
        return self.user_model.auth.get_xcams_auth_url()

    def update_view(self):
        self.given_name = self.user_model.get_given_name()
        self.given_name_bind.update_in_view(self.given_name)
        self.email = self.user_model.get_email()
        self.email_bind.update_in_view(self.email)
        self.logged_in = self.user_model.logged_in()
        self.logged_in_bind.update_in_view(self.logged_in)
