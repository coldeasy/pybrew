def get_test_alarms_config(**kwargs):
    return {
        'alarms': {
            'sms': {
                'twilio_acc_id': 123,
                'twilio_auth_token': '123',
                'respondents': ['00000000000'],
                'twilio_from': ['99999999999'],
            }
        }
    }


def get_test_config(**kwargs):
    return {
        'brew_thermometer_slave': '',
        'brew_temperature_update_interval': 10,
        'water_heater_gpio_pin': 16,
        'water_pump_gpio_pin': 16,
        'brew_temp_min': 17,
        'brew_temp_max': 22,
        "brew_temp_critical_max": 25,
        "brew_temp_critical_min": 15,
        'metrics': {
            'endpoint': 'localhost:514',
            'hmac_key': '5' * 32,
        }
    }
