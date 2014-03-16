import hmac
import struct
import hashlib
import socket
import msgpack


class Metrics(object):
    def __init__(self, config):
        self.host, self.port = config['endpoint'].split(':')
        self.port = int(self.port)
        self.hmac_key = str(config['hmac_key'].decode('base64'))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ipaddr = socket.gethostbyname(self.host)

    def _build_payload(self, key, value):
        msg = msgpack.packb((key, value))
        sig = hmac.new(self.hmac_key, msg, hashlib.sha256).digest()
        payload = sig + msg
        return struct.pack('!L', len(payload)) + payload

    def send(self, key, value=1):
        payload = self._build_payload(key, value)
        self.sock.sendto(payload, (self.ipaddr, self.port))
