
import jwt
import logging
from aiohttp import web
from trame.app import get_server
from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse

from launcher_app.app.config import TRAME_UCAMS_AUTH_URL, TRAME_UCAMS_REDIRECT_URL, TRAME_UCAMS_TOKEN_URL, \
    TRAME_UCAMS_SCOPES, TRAME_XCAMS_REDIRECT_URL, TRAME_XCAMS_SCOPES, TRAME_XCAMS_AUTH_URL, TRAME_XCAMS_TOKEN_URL, \
    TRAME_UCAMS_CLIENT_ID, TRAME_UCAMS_CLIENT_SECRET, TRAME_XCAMS_CLIENT_SECRET, TRAME_XCAMS_CLIENT_ID, EP_PATH

server = get_server()
server_state = server.state
server_state.is_authenticated = False


@server.controller.add("on_server_bind")
def app_available(wslink_server):
    """Add our custom REST endpoints to the trame server."""
    print(f"Add REST endpoint to ucams: {AuthManager().ucams_handler_path}")
    print(f"Add REST endpoint to xcams: {AuthManager().xcams_handler_path}")
    wslink_server.app.add_routes([web.get(AuthManager().ucams_handler_path, AuthManager().ucams_auth_handler),
                                  web.get(AuthManager().xcams_handler_path, AuthManager().xcams_auth_handler)])

class TrameAuth:

    def __init__(self):
        self.user_auth = {}
        self.xcams_session = None
        self.ucams_session = None
        self.xcams = False

        self.ucams_handler_path = ""
        self.xcams_handler_path = ""

        # list of callbacks that will get executed after a user logs in
        self.auth_listeners = []

    async def ucams_auth_handler(self, request):
        self.xcams = False
        await self.auth_handler(request, self.ucams_session, TRAME_UCAMS_TOKEN_URL, TRAME_UCAMS_CLIENT_SECRET)

    async def xcams_auth_handler(self, request):
        self.xcams = True
        await self.auth_handler(request, self.xcams_session, TRAME_XCAMS_TOKEN_URL, TRAME_XCAMS_CLIENT_SECRET)

    async def auth_handler(self, request, oauth_session, token_uri, secret):
        tokens = oauth_session.fetch_token(
            token_uri,
            authorization_response=str(request.url),
            client_secret=secret)
        self.user_auth = tokens
        server_state.is_authenticated = True
        userinfo = jwt.decode(tokens["id_token"], options={"verify_signature": False})
        self.user_auth["email"] = userinfo["email"]
        try:
            self.user_auth["given_name"] = userinfo["given_name"]
            self.user_auth["family_name"] = userinfo["family_name"]
        except:
            self.user_auth["given_name"] = userinfo["givenName"]
            self.user_auth["family_name"] = userinfo["sn"]
        for callback in self.auth_listeners:
            try:
                callback()
            except Exception as e:
                logging.warning(f"Could not update callback: {callback}. Error: {e}")
        raise web.HTTPFound(EP_PATH)


    def start_session(self, path_prefix="", session_id=""):
        self.ucams_session = OAuth2Session(TRAME_UCAMS_CLIENT_ID,
                                           redirect_uri=TRAME_UCAMS_REDIRECT_URL,
                                           scope=TRAME_UCAMS_SCOPES.split(" "),
                                           auto_refresh_url=TRAME_UCAMS_TOKEN_URL,
                                           token_updater=self.save_token,
                                           state=session_id)
        self.xcams_session = OAuth2Session(TRAME_XCAMS_CLIENT_ID,
                                           redirect_uri=TRAME_XCAMS_REDIRECT_URL,
                                           scope=TRAME_XCAMS_SCOPES.split(" "),
                                           auto_refresh_url=TRAME_XCAMS_TOKEN_URL,
                                           token_updater=self.save_token,
                                           state=session_id)

        self.ucams_handler_path = urlparse(TRAME_UCAMS_REDIRECT_URL).path
        self.xcams_handler_path = urlparse(TRAME_XCAMS_REDIRECT_URL).path

    def add_path_prefix_to_url(self, url=None, path_prefix=None):
        if path_prefix:
            new_path = path_prefix + urlparse(url).path
            return urlparse(url)._replace(path=new_path).geturl()
        return url


    def save_token(self, token):
        self.user_auth["access_token"] = token

    def get_token(self):
        if self.user_auth.get("access_token", None):
            try:
                # doing a request will refresh token if expired before attempting request
                if self.xcams:
                    self.xcams_session.get("")
                else:
                    self.ucams_session.get("")
            except:
                pass
            return self.user_auth["access_token"]
        else:
            return ""

    def logged_in(self):
        return self.get_token() != ""

    def get_email(self):
        return self.user_auth.get("email", "")

    def get_given_name(self):
        return self.user_auth.get("given_name", "Guest")

    def get_ucams_auth_url(self):
        try:
            auth_url_expanded, state = self.ucams_session.authorization_url(TRAME_UCAMS_AUTH_URL)

            return auth_url_expanded
        except:
            raise Exception("OAuth Session has not been started")

    def get_xcams_auth_url(self):
        try:
            auth_url_expanded, state = self.xcams_session.authorization_url(TRAME_XCAMS_AUTH_URL)

            return auth_url_expanded
        except:
            raise Exception("OAuth Session has not been started")

    def register_auth_listener(self, callback):
        self.auth_listeners.append(callback)


class AuthManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = TrameAuth()
        return cls._instance
