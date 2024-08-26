from bioblend import galaxy
from django.conf import settings


class GalaxyManager:

    def __init__(self):
        self.galaxy_instance = None

        self._connect_to_galaxy()

    def _connect_to_galaxy(self):
        try:
            if self.galaxy_instance is None:
                self.galaxy_instance = galaxy.GalaxyInstance(
                    url=settings.GALAXY_URL, key=settings.GALAXY_API_KEY
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
            active_jobs = self.galaxy_instance.jobs.get_jobs(self._get_history_id())

            print(active_jobs)
            return active_jobs
        except Exception as e:
            # If monitoring fails, reset the connection so that it can be re-established
            self.galaxy_instance = None
            raise e

    def stop_job(self, job_id):
        self._connect_to_galaxy()
        self.galaxy_instance.jobs.cancel_job(job_id)
