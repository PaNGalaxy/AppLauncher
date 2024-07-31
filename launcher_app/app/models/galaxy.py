import argparse
import logging
import requests
import threading

from bioblend import galaxy
from launcher_app.app.config import GALAXY_URL, GALAXY_API_KEY, GALAXY_HISTORY_ID, GALAXY_LAUNCHER_HISTORY_NAME, \
    GALAXY_API_KEY_ENDPOINT
from launcher_app.app.utilities.auth import AuthManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Galaxy:
    def _parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--galaxy-url", help="URL of the Galaxy server")
        parser.add_argument("--galaxy-key", help="API key for accessing the Galaxy server")
        parser.add_argument("--galaxy-history-id", help="Default Galaxy history ID to use")
        args, unknown = parser.parse_known_args()
        return args

    def sync_histories(self, periodic_update_sec=None, callback=None):
        try:
            self.galaxy_history_list = self.get_histories()
            if self.galaxy_current_history not in self.galaxy_history_list:
                self.galaxy_current_history = self.galaxy_history_list[0]
        except Exception:
            self.galaxy_current_history = None
            self.galaxy_history_list = []

        if callback:
            callback()

        if periodic_update_sec:
            thread = threading.Timer(periodic_update_sec, self.sync_histories, [periodic_update_sec, callback])
            thread.daemon = True
            thread.start()

    def _connect_to_galaxy(self):
        try:
            self.galaxy_instance = galaxy.GalaxyInstance(url=self.galaxy_url, key=self.galaxy_api_key)
        except:
            self.galaxy_instance = None
            return
        self.sync_histories()
        for history in self.galaxy_history_list:
            if history["id"] == self.initial_history:
                self.galaxy_current_history = history
                break

    def connect_to_galaxy_api(self):
        url = self.galaxy_url + GALAXY_API_KEY_ENDPOINT
        headers = {"Authorization": f"Bearer {AuthManager().get_token()}"}
        r = requests.get(url, headers=headers)
        self.galaxy_api_key = r.json()["api_key"]
        self._connect_to_galaxy()

    def __init__(self):
        args = self._parse_args()
        self.galaxy_current_history = None
        self.galaxy_url = args.galaxy_url or GALAXY_URL
        self.galaxy_api_key = args.galaxy_key or GALAXY_API_KEY
        self.initial_history = args.galaxy_history_id or GALAXY_HISTORY_ID
        if self.galaxy_api_key == "" or self.galaxy_api_key is None:
            AuthManager().register_auth_listener(self.connect_to_galaxy_api)
        else:
            self._connect_to_galaxy()

    def get_histories(self, name):
        histories = self.galaxy_instance.histories.get_histories(name=name)
        return [{"name": history["name"], "id": history["id"]} for history in histories]

    def get_history_id(self):
        history_name = GALAXY_LAUNCHER_HISTORY_NAME
        histories = self.get_histories(name=history_name)
        if len(histories) > 0:
            return histories[0]["id"]

        res = self.galaxy_instance.histories.create_history(history_name)
        return res["id"]

    async def invoke_interactive_tool(self, tool_id):
        self.galaxy_instance.tools.run_tool(self.get_history_id(), tool_id, {})

    async def stop_job(self, job_id):
        return self.galaxy_instance.jobs.cancel_job(job_id)

    def check_running_tools(self):
        history = self.get_history_id()
        history_contents = self.galaxy_instance.histories.show_history(history, contents=True, deleted=False,
                                                                       details="all")
        job_list = []
        entry_points = self.galaxy_instance.make_get_request(f"{self.galaxy_url}/api/entry_points?running=true")
        for dataset in history_contents:
            # dataset does not contain tool_id
            job_id = dataset['creating_job']
            job_info = self.galaxy_instance.jobs.show_job(job_id)
            if job_info['state'] == 'queued' or job_info['state'] == 'running':
                # Search entry points json for correct job listing and try to get the target url.
                target = None
                for ep in entry_points.json():
                    if ep["job_id"] == job_id:
                        target = ep.get("target", None)
                if target:
                    target = f"{self.galaxy_url}{target}"
                job_list.append(
                    {"job_id": job_id, "tool_id": job_info['tool_id'], "state": job_info['state'], "url": target})
        return job_list


class SharedGalaxy:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = Galaxy()
        return cls._instance
