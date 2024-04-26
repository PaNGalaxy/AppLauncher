import time
from bioblend import galaxy


def get_histories(state):
    galaxy_instance = galaxy.GalaxyInstance(url=state.galaxyURL, key=state.galaxyAPIKey)
    histories = galaxy_instance.histories.get_histories()
    return [{"name": history["name"], "id": history["id"]} for history in histories]


def invoke_interactive_tool(state, tool_id):
    histories = get_histories(state)
    current_history = histories[0]["id"]
    galaxy_instance = galaxy.GalaxyInstance(url=state.galaxyURL, key=state.galaxyAPIKey)
    dataset = galaxy_instance.tools.run_tool(current_history, tool_id, {})
    job_id = dataset["jobs"][0]["id"]
    if wait_for_job_running(galaxy_instance, job_id):
        # need extra sleep somtimes for entry points to be populated
        time.sleep(2)
        entry_points = galaxy_instance.make_get_request(f"{state.galaxyURL}/api/entry_points?running=true")
        target = None

        for ep in entry_points.json():
            if ep["job_id"] == job_id:
                target = ep["target"]
                break
        if target is not None:
            return f"{state.galaxyURL}{target}"
    return None

def wait_for_job_running(galaxy_instance, job_id, interval = 1, max_wait = 12000):
    # No built in way for BioBlend to wait for a job to start running (currently can only wait for terminal states)
    # returns true once job is running
    time_left = max_wait
    while galaxy_instance.jobs.get_state(job_id) != "running" and time_left > 0:
        time.sleep(interval)
        time_left -= interval
    if galaxy_instance.jobs.get_state(job_id) != "running":
        return False
    return True




