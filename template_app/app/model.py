# this is basically a dictionary with parameters that can be exchanged between server and client
class Model(dict):
    def __getattr__(self, key):
        return self[key]
    def __setattr__(self, key, value):
        self[key] = value

    def __init__(self):
        self.username = "test"
        self.run_number = 1

def prepare_config_file(model):
    s = ""
    for key, value in model.items():
        if isinstance(value, str):
            s += f"{key}='{value}'\n"
        else:
            s += f"{key}={value}\n"
    return s

def loadConfig(model, config_data):
    vars = {}
    exec(config_data, {}, vars)
    model.update(vars)
