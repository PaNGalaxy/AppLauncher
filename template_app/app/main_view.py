from trame.widgets import client
from trame.widgets import vuetify3 as vuetify
from .utilities import galaxy

class MainView:

    def __init__(self, state, server):
        self.state = state
        self.server = server
        self.ctrl = self.server.controller
        self.js_eval = client.JSEval(
                exec="window.location.href = $event"
        ).exec
        with vuetify.VRow(align="center"):
            button = vuetify.VBtn("Start Topaz Reduction tool", id="login-button-xcams", click=self.invoke_topaz_tool, style="padding: 10px; margin: 10px;")


    def invoke_topaz_tool(self):
        current_url = galaxy.invoke_interactive_tool(self.state, "neutrons_trame_topaz")
        if current_url is not None:
            self.js_eval(current_url)



