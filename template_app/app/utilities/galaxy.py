from bioblend import galaxy


def get_histories(config):
    galaxy_instance = galaxy.GalaxyInstance(url=config.state.galaxyURL, key=config.state.galaxyAPIKey)
    histories = galaxy_instance.histories.get_histories()
    return [{"name": history["name"], "id": history["id"]} for history in histories]
