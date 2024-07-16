import jwt
import logging
import os
from aiohttp import web
from trame.app import get_server
from requests_oauthlib import OAuth2Session

server = get_server()
server_state = server.state
server_state.is_authenticated = False

auth_url = os.getenv("TRAME_AUTH_URL", "http://localhost:8082/realms/master/protocol/openid-connect/auth")
token_url = os.getenv("TRAME_TOKEN_URL", "http://localhost:8082/realms/master/protocol/openid-connect/token")
client_id = os.getenv("TRAME_CLIENT_ID", "trame-demo")
client_secret = os.getenv("TRAME_CLIENT_SECRET", "tLVhtFouBjw7cKMbTXQEtJ89WabJcWAu")
redirect_uri = os.getenv("TRAME_REDIRECT_URL", "http://localhost:8080/redirect")

xcams_auth_url = os.getenv("TRAME_XCAMS_AUTH_URL", "http://localhost:8082/realms/master/protocol/openid-connect/auth")
xcams_token_url = os.getenv("TRAME_XCAMS_TOKEN_URL",
                            "http://localhost:8082/realms/master/protocol/openid-connect/token")
xcams_client_id = os.getenv("TRAME_XCAMS_CLIENT_ID", "trame-demo")
xcams_client_secret = os.getenv("TRAME_XCAMS_CLIENT_SECRET", "tLVhtFouBjw7cKMbTXQEtJ89WabJcWAu")
xcams_redirect_uri = redirect_uri + "/xcams"

app_path = os.getenv("EP_PATH", "/")
scopes = ["email", "profile", "openid", "User.Read"]


# @server.controller.add("on_server_bind")
# def app_available(wslink_server):
#     """Add our custom REST endpoints to the trame server."""
#     wslink_server.app.add_routes([web.get(AuthManager().ucams_handler_path, AuthManager().ucams_auth_handler),
#                                   web.get(AuthManager().xcams_handler_path, AuthManager().xcams_auth_handler)])
#     wslink = wslink_server


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
        await self.auth_handler(request, self.ucams_session, token_url, client_secret)

    async def xcams_auth_handler(self, request):
        self.xcams = True
        await self.auth_handler(request, self.xcams_session, xcams_token_url, xcams_client_secret)

    async def auth_handler(self, request, oauth_session, token_uri, secret):
        tokens = oauth_session.fetch_token(
            token_uri,
            authorization_response=str(request.url),
            client_secret=secret)
        self.user_auth = tokens
        server_state.is_authenticated = True
        userinfo = jwt.decode(tokens["id_token"], options={"verify_signature": False})
        self.user_auth["email"] = userinfo["email"]
        self.user_auth["given_name"] = userinfo["given_name"]
        self.user_auth["family_name"] = userinfo["family_name"]
        for callback in self.auth_listeners:
            try:
                callback()
            except:
                logging.warning("Could not update callback")
        raise web.HTTPFound(app_path)

    def start_session(self, handler_path=None):
        self.ucams_session = OAuth2Session(client_id,
                                           redirect_uri=redirect_uri,
                                           scope=scopes,
                                           auto_refresh_url=token_url,
                                           token_updater=self.save_token)
        self.xcams_session = OAuth2Session(xcams_client_id,
                                           redirect_uri=xcams_redirect_uri,
                                           scope=scopes,
                                           auto_refresh_url=xcams_token_url,
                                           token_updater=self.save_token)
        if handler_path:
            self.ucams_handler_path = handler_path
            self.xcams_handler_path = handler_path + "/xcams"

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
            auth_url_expanded, state = self.ucams_session.authorization_url(auth_url)

            return auth_url_expanded
        except:
            raise Exception("OAuth Session has not been started")

    def get_xcams_auth_url(self):
        try:
            auth_url_expanded, state = self.xcams_session.authorization_url(xcams_auth_url)

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
