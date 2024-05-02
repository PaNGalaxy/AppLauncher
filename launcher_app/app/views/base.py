from trame.widgets import vuetify3
from trame.ui.vuetify3 import VAppLayout


class SinglePageLayout(VAppLayout):
    def __init__(self, _server, template_name="main", **kwargs):
        super().__init__(_server, template_name=template_name, **kwargs)
        with self:
            with vuetify3.VLayout() as app_layout:
                self.app_layout = app_layout
                with vuetify3.VAppBar() as toolbar:
                    self.toolbar = toolbar
                    self.icon = vuetify3.VAppBarNavIcon()
                    self.title = vuetify3.VToolbarTitle("Trame application")

                self.content = vuetify3.VMain()

                with vuetify3.VFooter(
                    app=True, classes="my-0 py-0", border=True
                ) as footer:
                    self.footer = footer

    def on_server_reload(self):
        self.server.controller.on_server_reload(self.server)
