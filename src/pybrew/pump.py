import time
import logging


logger = logging.getLogger("pybrew.pump")


class Pump(object):
    def __init__(self, gpio, pump_max_on_seconds=None,
                 pump_seconds_between_on=None):
        self._gpio = gpio
        self._last_gpio_change_time = None
        self.max_on_seconds = pump_max_on_seconds or 60
        self.min_seconds_between_on = pump_seconds_between_on or 60
        logger.debug("Max on seconds %s", self.max_on_seconds)
        logger.debug("Min time between on %s", self.min_seconds_between_on)

    @property
    def is_on(self):
        return self._gpio.is_on

    def on(self):
        now = time.time()

        if self._last_gpio_change_time is None:
            logger.debug("Pump:starting")
            self._gpio.on()
            self._last_gpio_change_time = now
        elif not self.is_on and (now - self._last_gpio_change_time
                                 > self.min_seconds_between_on):
            logger.debug("Pump:restarting")
            logger.debug("last start time %s, now %s. Elapsed %s.",
                         self._last_gpio_change_time,
                         now,
                         now - self._last_gpio_change_time)
            self._gpio.on()
            self._last_gpio_change_time = now
        elif self.is_on and (now - self._last_gpio_change_time
                             > self.max_on_seconds):
            logger.debug("Pump:stopping")
            logger.debug("last start time %s, now %s. Elapsed %s.",
                         self._last_gpio_change_time,
                         now,
                         now - self._last_gpio_change_time)
            self._last_gpio_change_time = now
            self._gpio.off()

    def off(self):
        self._gpio.off()
