from trame.widgets import vuetify3 as vuetify

tab1_input_fields = [
    [{"label": "User Name", "variable": "model.username",
      "type": "text"}],
]

tab2_input_fields = [
    [{"label": "Run Number", "variable": "model.run_number",
      "type": "text"}],
    [{"label": "Galaxy History", "variable": "galaxyHistory",
      "type": "select", "options": []}],
]

class ConfigPanelTab:
    def __init__(self, input_fields):
        two_col = False
        for row_fields in input_fields:
            if len(row_fields) == 2:
                two_col = True
                break
        for row_fields in input_fields:
            with vuetify.VRow(align="center"):
                for field in row_fields:
                    with vuetify.VCol(cols="12", sm="6", md="3" if two_col else "6"):
                        vuetify.VLabel(field["label"], density="compact")
                    with vuetify.VCol(cols="12", sm="6", md="3" if two_col else "6",
                                      classes="flex-grow-1 flex-shrink-1"):
                        if field["type"] == "file":
                            vuetify.VFileInput(
                                v_model=field["variable"],
                                update_modelValue="flushState('model')",
                                density="compact", prepend_icon="", hide_details="true")
                        elif field["type"] == "select":
                            vuetify.VSelect(v_model=field["variable"],
                                            items=("items_"+field["variable"], field["options"]),
                                            item_title="name",
                                            item_value="id",
                                            return_object=True,
                                            update_modelValue="flushState('model')",
                                            density="compact",
                                            hide_details="true")
                        elif field["type"] == "password":
                            vuetify.VTextField(
                                v_model=field["variable"],
                                update_modelValue="flushState('model')",
                                density="compact", type=field["type"], hide_spin_buttons="true",
                                hide_details="true")
                        else:
                            vuetify.VTextField(
                                v_model=field["variable"],
                                update_modelValue="flushState('model')",
                                density="compact", type=field["type"], hide_spin_buttons="true",
                                hide_details="true")

class ConfigPanel():
    def __init__(self):
        with vuetify.VCard(classes="rounded-0"):
            with vuetify.VTabs(
                    v_model=("active_tab", 0),
                    bg_color="primary",
                    slider_color="red"
            ):
                vuetify.VTab("Tab 1", value=1)
                vuetify.VTab("Tab 2", value=2)
            with vuetify.VContainer(fluid=True):
                with vuetify.VWindow(v_model="active_tab"):
                    with vuetify.VWindowItem(value=1, reverse_transition="false", transition="false"):
                        ConfigPanelTab(tab1_input_fields)
                    with vuetify.VWindowItem(value=2, reverse_transition="false", transition="false"):
                        ConfigPanelTab(tab2_input_fields)