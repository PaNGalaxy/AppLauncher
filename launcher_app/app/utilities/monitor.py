import asyncio
import typing

import trame_server.utils.asynchronous


class TaskMonitor:

    def __init__(self, func: typing.Callable, update_frequency: int):
        self._func = func
        self._update_frequency = update_frequency
        self._run_monitor = False
        self._monitor_task = None

    def start_monitor(self):
        if self._run_monitor:
            return
        self._run_monitor = True
        self._monitor_task = trame_server.utils.asynchronous.create_task(self._monitor())

    def stop_monitor(self):
        self._run_monitor = False

    async def _monitor(self):
        while self._run_monitor:
            self._func()
            await asyncio.sleep(self._update_frequency)
