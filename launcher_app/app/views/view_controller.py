from trame_router.ui.router import RouterViewLayout

from launcher_app.app.views.routes import CategoryView, HomeView


class ViewController:
    def __init__(self, server, view_model):
        self.server = server
        self.vm = view_model

        self.create_routes()

    def create_routes(self):
        with RouterViewLayout(self.server, "/"):
            HomeView(self.server, self.vm)

        with RouterViewLayout(self.server, "/category/:category"):
            CategoryView(self.server, self.vm)
