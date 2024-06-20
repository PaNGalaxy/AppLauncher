from trame.widgets import vuetify3 as vuetify

from launcher_app.app.view_models.user import UserViewModel


class LogoutToolbar:

    def __init__(self, user_vm: UserViewModel):
        self.user_vm = user_vm
        self.user_vm.username_bind.connect("username")
        self.user_vm.email_bind.connect("email")
        self.user_vm.logged_in_bind.connect("is_logged_in")
        self.create_ui()

    def create_ui(self):
        with vuetify.VRow(align="right"):
            vuetify.VSpacer()
            vuetify.VBtn("{{username}}", readonly=True, v_show="is_logged_in", flat=True)
            vuetify.VBtn("Log Out", id="login-button", href="", flat=True, classes="sign-in-btn", v_show="is_logged_in",
                         style="margin-right: 2em;")


class LoginView:

    def __init__(self, user_vm: UserViewModel):
        self.user_vm = user_vm
        self.user_vm.username_bind.connect("username")
        self.user_vm.email_bind.connect("email")
        self.user_vm.logged_in_bind.connect("is_logged_in")
        self.create_ui()

    def create_ui(self):
        with vuetify.VContainer(style="height: 100%;",v_show="!is_logged_in"):
            with vuetify.VRow(align="right"):
                vuetify.VBtn("Sign In with UCAMS", id="ucams-login-button", href=self.user_vm.get_auth_url(), flat=True,
                             classes="sign-in-btn", style="margin-right: 2em;")
                vuetify.VBtn("Sign In with XCAMS", id="xcams-login-button", href=self.user_vm.get_xcams_auth_url(), flat=True, classes="sign-in-btn",
                             style="margin-right: 2em;")

