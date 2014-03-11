import logging
from twilio.rest import TwilioRestClient


logger = logging.getLogger('brew.alarm')


def _build_text_msg_alarm(config):
    def alarm(msg):
        client = TwilioRestClient(config['twilio_acc_id'],
                                  config['twilio_auth_token'])
        for respondent in config['respondents']:
            try:
                msg = client.messages.create(
                    to=respondent,
                    from_=config['twilio_from'],
                    body=msg
                )
            except:
                logger.critical("Could not contact respondent %s to respond "
                                "to brew emergency!" % respondent,
                                exc_info=True)
    return alarm


def build_alarms(config):
    alarms_config = config.get('alarms', {})
    if not alarms_config:
        return []

    alarms = []
    if 'SMS' in alarms:
        alarms.append(_build_text_msg_alarm(alarms['SMS']))

    return alarms


class TemperatureAlarm(object):
    def __init__(self, config):
        self.alarms = build_alarms(config)

    def me_brew_is_fecked(self, brew_temp, _brew_temp_critical_range):
        msg = "Help!! My homebrew temperature (%s) is critical!" % brew_temp
        for alarm in self.alarms:
            alarm(msg)
