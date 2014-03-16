import mock
import unittest
from pybrew.alarm import TemperatureAlarm
from tests import data


class AlarmsTestCase(unittest.TestCase):
    def setUp(self):
        super(AlarmsTestCase, self).setUp()
        self.config = data.get_test_alarms_config()
        self.alarm = TemperatureAlarm(self.config)

    def test_sends_twilio_sms(self):
        with mock.patch('pybrew.alarm.TwilioRestClient') as mock_client:
            self.alarm.me_brew_is_fecked(0, 0)

        self.assertTrue(mock_client.called)
