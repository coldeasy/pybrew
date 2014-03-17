import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)


def cleanup():
    GPIO.cleanup()


class GPIOOutput(object):
    """docstring for GPIO"""
    def __init__(self, pin_number):
        self.pin_number = pin_number
        GPIO.setup(self.pin_number, GPIO.OUT)
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    def _set_gpio_value(self, turn_on):
        if turn_on is self.is_on:
            return

        gpio_val = GPIO.HIGH if turn_on else GPIO.LOW
        GPIO.output(self.pin_number, gpio_val)
        self._is_on = turn_on

    def on(self):
        self._set_gpio_value(True)

    def off(self):
        self._set_gpio_value(False)
