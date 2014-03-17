import time
import logging

from pybrew import metrics

logger = logging.getLogger("pybrew")


class Counter(object):
    def __init__(self, config):
        super(Counter, self).__init__()
        self.input_file = open(config['input_file_path'], 'rb')
        self.output_file = open(config.get('output_file_path'), 'a')
        self.measurement_interval = config.get('measurement_interval', 1)
        self.metrics = metrics.Metrics(config['metrics'])

        logger.debug("Configured CO2 Counter with\n"
                     "InputFile (%s)\n"
                     "OutputFile (%s)\n"
                     "Measurement Interval (%s)" % (
                         self.input_file,
                         self.output_file,
                         self.measurement_interval
                     ))

    def run(self):
        running_records = []
        while True:
            status, dx, dy = tuple(ord(c) for c in self.input_file.read(3))
            running_records.append((time.time(), status, dx, dy))

            co2_emitted = self.check_co2_emitted(running_records)
            if co2_emitted:
                logger.info("co2_emitted")
                self.metrics.send('co2_emitted', 1)

            self._record_metrics(status, dx, dy)

    def _record_metrics(self, status, dx, dy):
        dx2 = dx - ((0x80 & dx) << 1)
        dy2 = dy - ((0x80 & dy) << 1)
        msg = ("TIME:%s, STATUS:%#02x, DX:DY(%d:%d), "
               "DX2:DY2(%d:%d)"
               % (time.time(), status, dx, dy, dx2, dy2))
        logger.debug(msg)

        if self.output_file:
            self.output_file.write(msg + '\n')
            self.output_file.flush()

    @staticmethod
    def check_co2_emitted(measurements):
        return False
