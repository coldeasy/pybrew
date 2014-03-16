import time
from pybrew import metrics


class Counter(object):
    """docstring for Counter"""
    def __init__(self, config):
        super(Counter, self).__init__()
        self.input_file_path = config['input_file_path']
        self.write_file_path = config.get('output_file_path')
        self.measurement_interval = config.get('measurement_interval', 1)
        self.metrics = metrics.Metrics(config['metrics'])

    def run(self):
        fp = file(self.input_file_path)

        if self.write_file_path:
            out_fp = file(self.write_file_path)
        else:
            out_fp = None

        running_records = []
        while True:
            status, dx, dy = tuple(ord(c) for c in fp.read(3))
            running_records.append((time.time(), status, dx, dy))

            co2_emitted = self.check_co2_emitted(running_records)
            if co2_emitted:
                self.metrics.send('co2_emitted', 1)

            dx2 = dx - ((0x80 & dx) << 1)
            dy2 = dy - ((0x80 & dy) << 1)
            if out_fp:
                out_fp.write("TIME:%s, STATUS:%#02x, DX:DY(%d:%d), "
                             "DX2:DY2(%d:%d)\n"
                             % (time.time(), status, dx, dy, dx2, dy2))
                out_fp.flush()

    @staticmethod
    def check_co2_emitted(measurements):
        pass
