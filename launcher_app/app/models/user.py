from launcher_app.app.models.galaxy import SharedGalaxy
from launcher_app.app.utilities.auth import TrameAuth as auth

class UserModel:
    def __int__(self):
        # will store user info. just importing galaxy here as placeholder, we might not need it at all
        self.galaxy = SharedGalaxy()

    def get_email(self):
        try:
            return auth.get_email()
        except:
            return ""

    def get_username(self):
        try:
            return auth.get_username()
        except:
            return ""

    def get_auth_url(self):
        return auth.get_auth_url()

    def logged_in(self):
        return auth.logged_in()
