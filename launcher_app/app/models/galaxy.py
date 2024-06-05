import argparse
import asyncio
import logging
import os
import threading

from bioblend import galaxy

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LAUNCHER_HISTORY_NAME = "launcher_history"

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

    def _connect_to_galaxy(self, args):
        self.galaxy_url = args.galaxy_url or os.getenv("GALAXY_URL")
        self.galaxy_api_key = args.galaxy_key or os.getenv("GALAXY_API_KEY")
        initial_history = args.galaxy_history_id or os.getenv("GALAXY_HISTORY_ID")
        try:
            self.galaxy_instance = galaxy.GalaxyInstance(url=self.galaxy_url, key=self.galaxy_api_key)
        except:
            self.galaxy_instance = None
        self.sync_histories()
        for history in self.galaxy_history_list:
            if history["id"] == initial_history:
                self.galaxy_current_history = history
                break

    def __init__(self):
        args = self._parse_args()
        self.galaxy_current_history = None
        self._connect_to_galaxy(args)

    def get_histories(self, name):
        histories = self.galaxy_instance.histories.get_histories(name=name)
        return [{"name": history["name"], "id": history["id"]} for history in histories]

    def get_history_id(self):
        history_name = LAUNCHER_HISTORY_NAME
        histories = self.get_histories(name=history_name)
        if len(histories) > 0:
            return histories[0]["id"]

        res = self.galaxy_instance.histories.create_history(history_name)
        return res["id"]

    async def invoke_interactive_tool(self, tool_id):
        dataset = self.galaxy_instance.tools.run_tool(self.get_history_id(), tool_id, {})

    async def stop_job(self, job_id):
        return self.galaxy_instance.jobs.cancel_job(job_id)

    def check_running_tools(self):
        history = self.get_history_id()
        history_contents = self.galaxy_instance.histories.show_history(history, contents=True, deleted=False, details="all")
        job_list = []
        entry_points = self.galaxy_instance.make_get_request(f"{self.galaxy_url}/api/entry_points?running=true")
        for dataset in history_contents:
            # dataset does not contain tool_id
            job_id = dataset['creating_job']
            job_info = self.galaxy_instance.jobs.show_job(job_id)
            if job_info['state'] == 'queued' or job_info['state'] == 'running':
                try:
                    target = next(filter(lambda x: x["job_id"] == job_id, entry_points.json())).get("target", None)
                except StopIteration:
                    target = None
                if target:
                    target = f"{self.galaxy_url}{target}"
                job_list.append({"job_id": job_id, "tool_id": job_info['tool_id'], "state": job_info['state'], "url": target})
        return job_list

class SharedGalaxy:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = Galaxy()
        return cls._instance
