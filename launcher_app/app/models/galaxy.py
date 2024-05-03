import argparse
import asyncio
import logging
import os
import threading

from bioblend import galaxy

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

    def get_histories(self):
        histories = self.galaxy_instance.histories.get_histories()
        return [{"name": history["name"], "id": history["id"]} for history in histories]

    async def invoke_interactive_tool(self, tool_id):
        histories = self.get_histories()
        current_history = histories[0]["id"]
        dataset = self.galaxy_instance.tools.run_tool(current_history, tool_id, {})
        job_id = dataset["jobs"][0]["id"]
        running = await self.wait_for_job_running(job_id)
        if running:
            # need extra sleep somtimes for entry points to be populated
            await asyncio.sleep(2)
            entry_points = self.galaxy_instance.make_get_request(f"{self.galaxy_url}/api/entry_points?running=true")
            target = None
            for ep in entry_points.json():
                if ep["job_id"] == job_id:
                    target = ep["target"]
                    break
            if target is not None:
                return f"{self.galaxy_url}{target}", job_id
        return None, None

    async def wait_for_job_running(self, job_id, interval=1, max_wait=12000):
        # No built in way for BioBlend to wait for a job.py to start running (can only wait for terminal states)
        # returns true once job.py is running
        time_left = max_wait
        while self.galaxy_instance.jobs.get_state(job_id) != "running" and time_left > 0:
            await asyncio.sleep(interval)
            time_left -= interval
        if self.galaxy_instance.jobs.get_state(job_id) != "running":
            return False
        return True

    async def stop_job(self, job_id):
        return self.galaxy_instance.jobs.cancel_job(job_id)

class SharedGalaxy:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = Galaxy()
        return cls._instance
