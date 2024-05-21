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
app_path = os.getenv("EP_PATH", "/")
scopes = ["email", "profile", "openid", "User.Read"]


class TrameAuth:
    user_auth = {}
    oauth_session = None
    state = ""
    handler_path = ""

    # list of callbacks that will get executed after a user logs in
    auth_listeners = []

    async def auth_handler(request):
        tokens = TrameAuth.oauth_session.fetch_token(
            token_url,
            authorization_response=str(request.url),
            client_secret=client_secret)
        print(tokens)
        TrameAuth.user_auth = tokens
        server_state.is_authenticated = True
        userinfo = jwt.decode(tokens["id_token"], options={"verify_signature": False})
        print(userinfo)
        TrameAuth.user_auth["email"] = userinfo["email"]
        TrameAuth.user_auth["username"] = userinfo["preferred_username"]
        for callback in TrameAuth.auth_listeners:
            try:
                callback()
            except:
                logging.warning("Could not update callback")
        raise web.HTTPFound(app_path)

    @server.controller.add("on_server_bind")
    def app_available(wslink_server):
        """Add our custom REST endpoints to the trame server."""
        wslink_server.app.add_routes([web.get(TrameAuth.handler_path, TrameAuth.auth_handler)])
        wslink = wslink_server

    def start_session(handler_path):
        TrameAuth.oauth_session = OAuth2Session(client_id,
                                                redirect_uri=redirect_uri,
                                                scope=scopes,
                                                auto_refresh_url=token_url,
                                                token_updater=TrameAuth.save_token)
        TrameAuth.handler_path = handler_path

    def save_token(token):
        TrameAuth.user_auth['access_token'] = token

    def get_token():
        # TODO: REFRESH TOKEN IF EXPIRED
        if TrameAuth.user_auth.get('access_token', None):
            try:
                # doing a request will refresh token if expired before attempting request
                TrameAuth.oauth_session.get("")
            except:
                pass
            return TrameAuth.user_auth['access_token']
        else:
            return ""

    def logged_in():
        return TrameAuth.get_token() != ""

    def get_email():
        return TrameAuth.user_auth.get("email", "")

    def get_username():
        return TrameAuth.user_auth.get("username", "")

    def get_auth_url():
        try:
            auth_url_expanded, state = TrameAuth.oauth_session.authorization_url(auth_url)
            return auth_url_expanded
        except:
            raise Exception("OAuth Session has not been started")

    def register_auth_listner(callback):
        TrameAuth.auth_listeners.append(callback)
