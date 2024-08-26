from django.conf import settings
from requests_oauthlib import OAuth2Session


class AuthManager:

    def __init__(self):
        self.auth_token = None
        self.ucams_session = OAuth2Session(
            settings.UCAMS_CLIENT_ID,
            redirect_uri=settings.UCAMS_REDIRECT_URL,
            scope=settings.UCAMS_SCOPES.split(" "),
            auto_refresh_url=settings.UCAMS_TOKEN_URL,
            token_updater=self.save_token,
        )
        self.xcams_session = OAuth2Session(
            settings.XCAMS_CLIENT_ID,
            redirect_uri=settings.XCAMS_REDIRECT_URL,
            scope=settings.XCAMS_SCOPES.split(" "),
            auto_refresh_url=settings.XCAMS_TOKEN_URL,
            token_updater=self.save_token,
        )

    def save_token(self, token):
        self.auth_token = token

    def get_ucams_auth_url(self):
        return self.ucams_session.authorization_url(settings.UCAMS_AUTH_URL)[0]

    def get_xcams_auth_url(self):
        return self.xcams_session.authorization_url(settings.XCAMS_AUTH_URL)[0]
