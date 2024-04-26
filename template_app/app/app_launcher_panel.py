from trame.widgets import vuetify3 as vuetify


class AppLauncherPanel:

	def __init__(self, input_fields):
		with vuetify.VCol(cols="12", sm="6", md="3" if two_col else "6"):
                        vuetify.VLabel("Launch apps from here", density="compact")
