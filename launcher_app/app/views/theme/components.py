from trame.widgets import vuetify3 as vuetify
from trame_client.widgets import html


class CustomComponents:
    def Footer(layout):
        with layout.footer as footer:
            vuetify.VProgressCircular(
                classes="ml-n3 mr-1",
                color="primary",
                indeterminate=("!!galaxy_running",),
                size=16,
                width=3,
            ),
            html.A(
                "Powered by Calvera",
                classes="text-grey-lighten-1 text-caption text-decoration-none",
                href=("galaxyLink",),
                target="_blank")
            vuetify.VSpacer()
            footer.add_child(
                '<a href="https://www.ornl.gov/" class="text-grey-lighten-1 text-caption text-decoration-none" '
                'target="_blank">© 2024 ORNL</a>'
        )

    def List(action=None, header=None, **kwargs):
        with vuetify.VList():
            if header is not None:
                vuetify.VListSubheader(header)
            with vuetify.VListItem(classes="pa-2", **kwargs):
                with vuetify.Template(v_slot_append=True, v_if=action is not None):
                    with vuetify.VListItemAction():
                        if callable(action):
                            action()