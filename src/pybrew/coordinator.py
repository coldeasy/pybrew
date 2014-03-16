from pybrew import metrics
from pybrew import temperatures
from pybrew import alarm
from pybrew import gpio


class Coordinator(object):
    def __init__(self, config):
        self.config = config
        self.metrics = metrics.Metrics(config['metrics'])
        self.temp_alarm = alarm.TemperatureAlarm(config)
        self.brew_temp_monitor = temperatures.Temperature(
            config['brew_thermometer_slave'],
            config['brew_temperature_update_interval'],
            metrics.Metrics(config['metrics'])
        )

        # self.water_temp_monitor = temperatures.Temperature(
        #     gpio.GPIO(config['water_gpio_pin'])
        # )
        self.water_heater = gpio.GPIOOutput(
            config['water_heater_gpio_pin']
        )

        self.water_pump = gpio.GPIOOutput(
            config['water_pump_gpio_pin']
        )

        self.brew_temp_range = (
            float(config['brew_temp_min']),
            float(config['brew_temp_max']),
        )

        self.brew_temp_critical_range = (
            float(config['brew_temp_critical_min']),
            float(config['brew_temp_critical_max']),
        )

    @property
    def brew_temp_min(self):
        return self.brew_temp_range[0]

    @property
    def brew_temp_max(self):
        return self.brew_temp_range[1]

    @property
    def brew_temp_critical_min(self):
        return self.brew_temp_critical_range[0]

    @property
    def brew_temp_critical_max(self):
        return self.brew_temp_critical_range[1]

    def _brew_temp_out_of_range(self, brew_temp):
        in_range = (
            self.brew_temp_min <= brew_temp <= self.brew_temp_max
        )
        return not in_range

    def _maybe_send_alarms(self, brew_temp):
        in_range = (
            self.brew_temp_critical_min <= brew_temp <= self.brew_temp_critical_max
        )
        if in_range:
            return

        self.temp_alarm.me_brew_is_fecked(brew_temp,
                                          self.brew_temp_critical_range)

    def _heat_brew(self, brew_temp):
        self.water_pump.on()
        self.water_heater.on()
        self.metrics.send('heating', 1)

    def _cool_brew(self, brew_temp):
        self.water_pump.off()
        self.water_heater.off()
        self.metrics.send('heating', 0)

    def run(self):
        brew_temp = self.brew_temp_monitor.temperature
        if not self._brew_temp_out_of_range(brew_temp):
            return

        self._maybe_send_alarms(brew_temp)

        if brew_temp < self.brew_temp_min:
            self._heat_brew(brew_temp)
        elif brew_temp > self.brew_temp_max:
            self._cool_brew(brew_temp)
