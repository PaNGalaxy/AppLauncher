from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.utils.crypto import get_random_string
from jwt import decode
from requests_oauthlib import OAuth2Session

from launcher_app.models import OAuthSessionState


class AuthManager:

    def __init__(self, request):
        if request.user.is_authenticated:
            self.oauth_state = OAuthSessionState.objects.get(user=request.user)
        else:
            try:
                self.oauth_state = OAuthSessionState.objects.get(
                    state_param=request.GET["state"]
                )
            except (KeyError, OAuthSessionState.DoesNotExist):
                self.oauth_state = OAuthSessionState.objects.create(
                    state_param=self.create_state_param()
                )

        self.ucams_session = OAuth2Session(
            settings.UCAMS_CLIENT_ID,
            auto_refresh_url=settings.UCAMS_TOKEN_URL,
            redirect_uri=settings.UCAMS_REDIRECT_URL,
            scope=settings.UCAMS_SCOPES.split(" "),
            state=self.oauth_state.state_param,
            token_updater=self.save_token,
        )
        self.xcams_session = OAuth2Session(
            settings.XCAMS_CLIENT_ID,
            auto_refresh_url=settings.XCAMS_TOKEN_URL,
            redirect_uri=settings.XCAMS_REDIRECT_URL,
            scope=settings.XCAMS_SCOPES.split(" "),
            state=self.oauth_state.state_param,
            token_updater=self.save_token,
        )

    def create_state_param(self):
        return get_random_string(length=128)

    def login(self, request, email, given_name):
        try:
            user = get_user_model().objects.get(username=email)
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create_user(
                username=email, email=email, first_name=given_name
            )

        login(request, user)

        # Removing old session states both reduces the size of the database over
        # time and allows us to make OAuthSessionState.user a OneToOneField.
        OAuthSessionState.objects.filter(user=user).delete()

        self.oauth_state.user = user
        self.oauth_state.save()

    def redirect_handler(self, request, session_type):
        self.oauth_state.session_type = session_type
        self.oauth_state.save()

        match session_type:
            case "ucams":
                session = self.ucams_session
            case "xcams":
                session = self.xcams_session

        tokens = session.fetch_token(
            settings.UCAMS_TOKEN_URL,
            authorization_response=request.build_absolute_uri(),
            client_secret=settings.UCAMS_CLIENT_SECRET,
        )
        self.save_token(tokens["access_token"])

        # TODO: verify signature seems important???
        return decode(tokens["id_token"], options={"verify_signature": False})

    def get_token(self):
        try:
            # Refresh the token if necessary
            match self.oauth_state.session_type:
                case "ucams":
                    self.ucams_session.get("")
                case "xcams":
                    self.xcams_session.get("")
        except:
            pass

        return self.oauth_state.access_token

    def save_token(self, token):
        self.oauth_state.access_token = token
        self.oauth_state.save()

    def get_ucams_auth_url(self):
        return self.ucams_session.authorization_url(settings.UCAMS_AUTH_URL)[0]

    def get_xcams_auth_url(self):
        return self.xcams_session.authorization_url(settings.XCAMS_AUTH_URL)[0]
