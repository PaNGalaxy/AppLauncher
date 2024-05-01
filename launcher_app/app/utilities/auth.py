from aiohttp import web

from trame.app import get_server

from requests_oauthlib import OAuth2Session


server = get_server()
server_state = server.state
server_state.is_authenticated = False

auth_url = "http://localhost:8082/realms/master/protocol/openid-connect/auth"
token_url = 'http://localhost:8082/realms/master/protocol/openid-connect/token'
client_id = 'trame-demo'
client_secret = 'tLVhtFouBjw7cKMbTXQEtJ89WabJcWAu'
redirect_uri = 'http://localhost:8080/redirect'
scopes = ["email", "profile", "openid"]

class TrameAuth:

    user_auth = []
    oauth_session = None
    state = ""
    handler_path = "/redirect"

    async def auth_handler(request):
        tokens = TrameAuth.oauth_session.fetch_token(
            token_url,
            authorization_response=str(request.url),
            client_secret=client_secret)
        print(tokens)
        TrameAuth.user_auth = tokens
        server_state.is_authenticated = True
        raise web.HTTPFound("/")

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
        user_auth['access_token'] = token

    def get_token():
        # TODO: REFRESH TOKEN IF EXPIRED
        if user_auth['access_token']:
            try:
                # doing a request will refresh token if expired before attempting request
                oauth_session.get("")
            except:
                pass
            return user_auth['access_token']
        else:
            return ""

    def get_auth_url():
        try:
            auth_url_expanded, state = TrameAuth.oauth_session.authorization_url(auth_url)
            return auth_url_expanded
        except:
            raise Exception("OAuth Session has not been started")


