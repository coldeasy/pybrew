import hmac
import hashlib
import socket
import msgpack


class Metrics(object):
    def __init__(self, config):
        self.host, self.port = config['metrics_endpoint'].split(':')
        self.hmac_key = config['hmac_key']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ipaddr = socket.gethostbyname(self.host)

    def _build_payload(self, key, value):
        msg = msgpack.packb((key, value))
        sig = hmac.new(self.hmac_key, msg, hashlib.sha256).digest()
        return sig + msg

    def send(self, key, value=1):
        payload = self._build_payload(key, value)
        self.sock.sendto(payload, self.ipaddr)
