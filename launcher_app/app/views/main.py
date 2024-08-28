from py_mvvm.trame_binding import TrameBinding
from trame_facade import ThemedApp

from trame.app import get_server
from trame.decorators import TrameApp
from trame.widgets import client, html, router, vuetify3 as vuetify

from launcher_app.app.mvvm_factory import create_viewmodels
from launcher_app.app.utilities.auth import AuthManager
from launcher_app.app.views.view_controller import ViewController


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


@TrameApp()
class App(ThemedApp):
    def __init__(self, server=None):
        super().__init__(server=server)
        self.server = get_server(server, client_type="vue3")
        self.ctrl = self.server.controller
        self.server.cli.add_argument("--session", help="Session identifier")
        args, _ = self.server.cli.parse_known_args()
        self.session = args.session
        self.port = args.port
        self.session_key = args.authKey
        self.full_redirect_path = f"/api/{args.session}"

        print(self.full_redirect_path)
        print(self.session_key)
        binding = TrameBinding(self.server.state)
        self.vm = create_viewmodels(binding)

        self.auth = AuthManager()
        self.auth.start_session(path_prefix=self.full_redirect_path, session_id=self.session)

        self.view_controller = ViewController(self.server, self.vm, self.vuetify_config)
        self.create_ui()


    @property
    def state(self):
        return self.server.state

    def create_ui(self):
        self.state.trame__title = "Neutrons App Dashboard"

        with super().create_ui() as layout:
            client.ClientTriggers(
                mounted=(
                    f"""
                    window.document.cookie = 'trame_launcher_session={self.session}';
                    window.document.cookie = 'trame_launcher_port={self.port}';
                    window.document.cookie = 'trame_session_key={self.session_key}';
                    """
                )
            )
            with layout.toolbar:
                layout.toolbar_title.set_text(
                    "{{ tools !== undefined && $route.params.category !== undefined ? `${tools[$route.params.category]['name']} Applications` : 'Neutrons App Dashboard' }}"
                )

                with layout.actions:
                    html.Span(
                        "Welcome, {{ given_name }}",
                        v_if="is_logged_in",
                        classes="pr-2 text-button",
                    )
                    with vuetify.VMenu(
                        v_else=True, close_delay=10000, open_on_hover=True
                    ):
                        with vuetify.Template(v_slot_activator="{ props }"):
                            with vuetify.VBtn(v_bind="props"):
                                html.Span("Sign In")
                        with vuetify.VList():
                            vuetify.VListItem(
                                "via UCAMS",
                                href=self.vm["user"].get_auth_url(),
                            )
                            vuetify.VListItem(
                                "via XCAMS",
                                href=self.vm["user"].get_xcams_auth_url(),
                            )

                    with vuetify.VMenu(
                        v_if="is_logged_in", close_on_content_click=False
                    ):
                        with vuetify.Template(v_slot_activator="{ props }"):
                            vuetify.VBtn(v_bind="props", icon="mdi-cogs")
                        with vuetify.VCard(title="Preferences", width=400):
                            with vuetify.VCardText():
                                vuetify.VSwitch(
                                    v_model="auto_open",
                                    hide_details=True,
                                    label="Automatically Open Tools in a New Tab After Launch",
                                    click=(
                                        self.vm["home"].set_local_storage,
                                        "[{'auto_open': !auto_open}]",
                                    ),
                                )
                                html.P(
                                    (
                                        "If tools don't automatically open after launching, then you "
                                        "may need to allow pop-ups on this site in your browser or "
                                        "browser extension settings."
                                    ),
                                    v_if="auto_open",
                                    classes="text-caption",
                                )

            with layout.content:
                router.RouterView()

            return layout
