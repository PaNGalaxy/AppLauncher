from django.conf import settings
from django.contrib.auth import get_user_model, login
from jwt import decode
from requests_oauthlib import OAuth2Session


class AuthManager:

    def __init__(self):
        self.auth_token = None
        self.current_session = None
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

    def login(self, request, email, given_name):
        try:
            user = get_user_model().objects.get(username=email)
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create_user(
                username=email, email=email, first_name=given_name
            )
        login(request, user)

    def redirect_handler(self, request, session_type):
        match session_type:
            case "ucams":
                self.current_session = self.ucams_session
            case "xcams":
                self.current_session = self.xcams_session

        tokens = self.current_session.fetch_token(
            settings.UCAMS_TOKEN_URL,
            authorization_response=request.build_absolute_uri(),
            client_secret=settings.UCAMS_CLIENT_SECRET,
        )
        self.auth_token = tokens["access_token"]

        # TODO: verify signature seems important???
        return decode(tokens["id_token"], options={"verify_signature": False})

    def get_token(self):
        try:
            self.current_session.get("")  # Refresh the token if necessary
        except:
            pass

        return self.auth_token

    def save_token(self, token):
        self.auth_token = token

    def get_ucams_auth_url(self):
        return self.ucams_session.authorization_url(settings.UCAMS_AUTH_URL)[0]

    def get_xcams_auth_url(self):
        return self.xcams_session.authorization_url(settings.XCAMS_AUTH_URL)[0]
