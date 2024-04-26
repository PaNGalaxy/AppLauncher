from trame.widgets import vuetify3 as vuetify

from .auth import TrameAuth as auth

class LoginView:

    def __init__(self):
        with vuetify.VRow(align="center"):
            vuetify.VBtn("Login", id="login-button", href=auth.get_auth_url(), flat=True)