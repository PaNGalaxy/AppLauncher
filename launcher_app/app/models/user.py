from launcher_app.app.models.galaxy import SharedGalaxy
from launcher_app.app.utilities.auth import AuthManager


class UserModel:
    def __init__(self):
        # will store user info. just importing galaxy here as placeholder, we might not need it at all
        self.auth = AuthManager()
        self.galaxy = SharedGalaxy()

    def get_email(self):
        try:
            return self.auth.get_email()
        except:
            return ""

    def get_username(self):
        try:
            return self.auth.get_username()
        except:
            return ""

    def logged_in(self):
        return self.auth.logged_in()
