from py_mvvm.trame_binding import TrameBinding

from trame.app import get_server
from trame.assets.local import LocalFileManager
from trame.decorators import TrameApp
from trame.widgets import html, router, vuetify3 as vuetify

from launcher_app.app.mvvm_factory import create_viewmodels
from launcher_app.app.utilities.auth import AuthManager
from launcher_app.app.views.theme import ThemedApp
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
        self.state.trame__favicon = LocalFileManager(__file__).url(
            "favicon", "./theme/assets/favicon.png"
        )

        with super().create_ui() as layout:
            layout.theme.theme = (
                "tools !== undefined && $route.params.category !== undefined ? tools[$route.params.category]['theme'] : 'default'",
            )

            with layout.toolbar:
                layout.toolbar_title.set_text(
                    "{{ tools !== undefined && $route.params.category !== undefined ? `${tools[$route.params.category]['name']} Applications` : 'Neutrons App Dashboard' }}"
                )

            with layout.content:
                router.RouterView()

                return layout
