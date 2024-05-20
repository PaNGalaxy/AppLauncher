from trame.widgets import vuetify3 as vuetify

from launcher_app.app.utilities.auth import TrameAuth as auth


class LoginView:

    def __init__(self):
        with vuetify.VRow(align="right"):
            # TODO: need to connect auth object to to view model
            vuetify.VLabel(auth.get_email(), v_show="false")
            vuetify.VBtn("Sign In", id="login-button", href=auth.get_auth_url(), flat=True, classes="sign-in-btn")
            vuetify.VBtn("Log Out", id="login-button", href="", flat=True, classes="sign-in-btn", v_show="false")
