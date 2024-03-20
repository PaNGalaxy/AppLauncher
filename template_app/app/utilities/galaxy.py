from bioblend import galaxy


def get_histories(state):
    galaxy_instance = galaxy.GalaxyInstance(url=state.galaxyURL, key=state.galaxyAPIKey)
    histories = galaxy_instance.histories.get_histories()
    return [{"name": history["name"], "id": history["id"]} for history in histories]
