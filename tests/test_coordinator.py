import mock
import unittest
from pybrew.coordinator import Coordinator
from tests import data


class CoordinatorTestCase(unittest.TestCase):
    def setUp(self):
        super(CoordinatorTestCase, self).setUp()
        self.config = data.get_test_config()
        self.coordinator = Coordinator(self.config)

    def test_brew_temp_is_out_of_range(self):
        temp = self.config['brew_temp_min'] - 1

        out_of_range = self.coordinator._brew_temp_out_of_range(temp)

        self.assertTrue(out_of_range)

    def test_brew_out_of_range_heats_up(self):
        temp = self.config['brew_temp_min'] - 1

        with mock.patch.object(self.coordinator, '_heat_brew') as mock_heater:
            with mock.patch.object(self.coordinator, 'brew_temp_monitor') as (
                mock_monitor
            ):
                mock_monitor.temperature = temp
                self.coordinator.run()

        self.assertTrue(mock_heater.called)

    def test_brew_out_of_range_cools_down(self):
        temp = self.config['brew_temp_max'] + 1

        with mock.patch.object(self.coordinator, '_cool_brew') as mock_cooler:
            with mock.patch.object(self.coordinator, 'brew_temp_monitor') as (
                mock_monitor
            ):
                mock_monitor.temperature = temp
                self.coordinator.run()

        self.assertTrue(mock_cooler.called)

    def test_sends_alarms(self):
        temp = self.config['brew_temp_critical_min'] - 1

        with mock.patch.object(self.coordinator, 'temp_alarm') as mock_alarm:
            with mock.patch.object(self.coordinator, 'brew_temp_monitor') as (
                mock_monitor
            ):
                mock_monitor.temperature = temp
                self.coordinator.run()

        self.assertTrue(mock_alarm.me_brew_is_fecked.called)
