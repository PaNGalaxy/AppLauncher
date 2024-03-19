from trame.app import get_server
from trame.widgets import vuetify3 as vuetify

from .model import loadConfig, prepare_config_file

server = get_server()
state, ctrl = server.state, server.controller  # Extract server state and controller


class ExecutionPanel:
    def __init__(self):
        with vuetify.VContainer():
            with vuetify.VRow(justify="center"):
                with vuetify.VCol(cols="auto"):
                    vuetify.VFileInput(
                        v_model=("config_file", None),
                        classes="d-none",
                        ref="fread",
                    )
                    vuetify.VBtn("Read Configuration File",
                                 size="small",
                                 color="primary",
                                 click="trame.refs.fread.click()",
                                 )
                with vuetify.VCol(cols="auto"):
                    vuetify.VBtn("Write Configuration File",
                                 size="small",
                                 color="primary",
                                 click="utils.download('config.txt" + "', trigger('download_config'), 'text/plain')",
                                 )


@state.change("config_file")
def read_config_file(config_file, **_kwargs):
    if config_file is None:
        return
    config_data = config_file[0]['content'].decode("utf-8")
    loadConfig(server.state.model, config_data)
    server.state.dirty("model")
    server.state.config_file = None


@ctrl.trigger("download_config")
def generate_content():
    return prepare_config_file(server.state.model)
