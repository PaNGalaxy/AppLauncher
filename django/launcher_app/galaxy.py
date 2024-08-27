"""
Defines a class for interacting with a specified Galaxy server.

The server to connect to can be controlled via the GALAXY_URL setting.
The endpoint on the server through which to get a user's API key can be controlled via the GALAXY_API_KEY_ENDPOINT setting.
The history name to use for all jobs can be controlled via the GALAXY_HISTORY_NAME setting.
"""


from bioblend import galaxy
from django.conf import settings
from requests import get as requests_get

from launcher_app.auth import AuthManager


class GalaxyManager:
    """
    Manages a connection to Galaxy and provides methods for managing and monitoring Galaxy jobs.

    auth_manager is an instance of AuthManager that will be used to authenticate with Galaxy to get the user's API key.
    """

    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self.galaxy_instance = None

    def _connect_to_galaxy(self):
        try:
            if self.galaxy_instance is None:
                response = requests_get(
                    f"{settings.GALAXY_URL}{settings.GALAXY_API_KEY_ENDPOINT}",
                    headers={
                        "Authorization": f"Bearer {self.auth_manager.get_token()}"
                    },
                )
                api_key = response.json()["api_key"]

                self.galaxy_instance = galaxy.GalaxyInstance(
                    url=settings.GALAXY_URL, key=api_key
                )
        except:
            self.galaxy_instance = None

    def _get_history_id(self):
        histories = self.galaxy_instance.histories.get_histories(
            name=settings.GALAXY_HISTORY_NAME
        )
        if len(histories) > 0:
            return histories[0]["id"]

        result = self.galaxy_instance.histories.create_history(
            settings.GALAXY_HISTORY_NAME
        )
        return result["id"]

    def launch_job(self, tool_id):
        self._connect_to_galaxy()
        self.galaxy_instance.tools.run_tool(self._get_history_id(), tool_id, {})

    def monitor_jobs(self):
        try:
            self._connect_to_galaxy()

            history_contents = self.galaxy_instance.histories.show_history(
                self._get_history_id(), contents=True, deleted=False, details="all"
            )
            job_list = []
            entry_points = self.galaxy_instance.make_get_request(
                f"{settings.GALAXY_URL}/api/entry_points?running=true"
            )
            for dataset in history_contents:
                try:
                    # dataset does not contain tool_id
                    job_id = dataset["creating_job"]
                    job_info = self.galaxy_instance.jobs.show_job(job_id)
                    if (
                        job_info["state"] == "queued"
                        or job_info["state"] == "running"
                        or job_info["state"] == "error"
                    ):
                        # Search entry points json for correct job listing and try to get the target url.
                        target = None
                        for ep in entry_points.json():
                            if ep["job_id"] == job_id:
                                target = ep.get("target", None)
                        if target:
                            target = f"{settings.GALAXY_URL}{target}"
                        job_list.append(
                            {
                                "job_id": job_id,
                                "tool_id": job_info["tool_id"],
                                "state": job_info["state"],
                                "url": target,
                            }
                        )
                except:
                    # Some unusual datasets will cause issues. However, We still want to check other datasets.
                    continue
            return job_list
        except Exception as e:
            # If monitoring fails, reset the connection so that it can be re-established cleanly
            self.galaxy_instance = None
            raise e

    def stop_job(self, job_id):
        self._connect_to_galaxy()
        self.galaxy_instance.jobs.cancel_job(job_id)
