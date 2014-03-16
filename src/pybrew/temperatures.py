import re
import time
import threading
import logging


TEMP_RE_EXP = r't=(?P<temp>\d+)'
logger = logging.getLogger("pybrew")


class _TemperatureFetcher(threading.Thread):
    def __init__(self, slave_location, interval, metrics):
        super(_TemperatureFetcher, self).__init__()
        self.slave_location = slave_location
        self.interval = interval
        self.metrics = metrics
        self._temperature = None

    @property
    def temperature(self):
        return self._temperature

    def _update_temp_from_data(self, data):
        match = re.search(TEMP_RE_EXP, data)
        if not match:
            return

        self.temperature = int(match.group('temp'), base=10)
        self.metrics.send('brew_temp', self.temperature)

    def run(self):
        while True:
            with open(self.slave_location, 'r') as in_f:
                data = in_f.read()
                self._update_temp_from_data(data)
            time.sleep(self.interval)


class Temperature(object):
    def __init__(self, slave_location, fetch_interval, metrics):
        self._fetcher = _TemperatureFetcher(slave_location,
                                            fetch_interval,
                                            metrics)
        self._fetcher.daemon = True
        self._fetcher.start()

    @property
    def temperature(self):
        if self._fetcher.temperature is None:
            logger.critical("Temperature fetcher is not running!!")
        return self._fetcher.temperature
