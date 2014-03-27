import time


class Pump(object):
    def __init__(self, gpio, pump_max_on_seconds=None,
                 pump_seconds_between_on=None):
        self._gpio = gpio
        self._last_start_time = None
        self.max_on_seconds = pump_max_on_seconds or 60
        self.min_seconds_between_on = pump_seconds_between_on or 60

    @property
    def is_on(self):
        return self._gpio.is_on

    def on(self):
        if self._last_start_time is None:
            self._gpio.on()
            self._last_start_time = time.time()
        elif not self.is_on and (time.time() - self._last_start_time
                                 > self.min_seconds_between_on):
            self._gpio.on()
            self._last_start_time = time.time()
        elif self.is_on and (time.time() - self._last_start_time
                             > self.max_on_seconds):
            self._gpio.off()
        else:
            self._gpio.on()

    def off(self):
        self._gpio.off()
