import logging
from twilio.rest import TwilioRestClient
from zappa.core import mail


logger = logging.getLogger('brew.alarm')


def _build_email_msg_alarm(config):
    def alarm(msg):
        with mail.create_context(config['username'],
                                 config['password'],
                                 config['server'],
                                 config['port'],
                                 ) as mail_context:
            try:
                mail.send(mail_context,
                          config['from'],
                          config['respondents'],
                          subject='Brew Emergency',
                          text_body=msg)
            except:
                logger.critical("Could not contact respondent %s to respond "
                                "to brew emergency!" % config['respondents'],
                                exc_info=True)
    return alarm


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

    if 'email' in alarms_config:
        logger.info("Building email alarm")
        alarms.append(_build_email_msg_alarm(alarms_config['email']))
    if 'sms' in alarms_config:
        logger.info("Building sms alarm")
        alarms.append(_build_text_msg_alarm(alarms_config['sms']))

    return alarms


class TemperatureAlarm(object):
    def __init__(self, config):
        self.alarms = build_alarms(config)
        logger.info("Configured %d alarms", len(self.alarms))

    def me_brew_is_fecked(self, brew_temp, _brew_temp_critical_range):
        msg = "Help!! My homebrew temperature (%s) is critical!" % brew_temp
        for alarm in self.alarms:
            alarm(msg)
