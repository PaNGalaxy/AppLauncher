from trame_router.ui.router import RouterViewLayout

from launcher_app.app.views.routes import CategoryView, HomeView
from trame.widgets import vuetify3 as vuetify

class ViewController:
    def __init__(self, server, view_model, vuetify_config):
        self.server = server
        self.vm = view_model

        self.create_routes(vuetify_config)

    def create_routes(self, vuetify_config):
        with RouterViewLayout(self.server, "/"):
            HomeView(self.server, self.vm, vuetify_config)
            # vuetify.VTextField("Hello")
        with RouterViewLayout(self.server, "/category/:category"):
            CategoryView(self.server, self.vm)
            # vuetify.VTextField("Category")
