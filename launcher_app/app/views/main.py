from py_mvvm.trame_binding import TrameBinding
from trame_facade import ThemedApp

from trame.app import get_server
from trame.decorators import TrameApp
from trame.widgets import html, router, vuetify3 as vuetify

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
        binding = TrameBinding(self.server.state)
        self.vm = create_viewmodels(binding)
        self.auth = AuthManager()

        self.view_controller = ViewController(self.server, self.vm, self.vuetify_config)

        self.create_ui()

    @property
    def state(self):
        return self.server.state

    def create_ui(self):
        self.state.trame__title = "Neutrons App Dashboard"

        with super().create_ui() as layout:
            layout.theme.theme = (
                "tools !== undefined && $route.params.category !== undefined ? tools[$route.params.category]['theme'] : 'default'",
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

            with layout.content:
                router.RouterView()

            return layout
