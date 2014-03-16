import hmac
import struct
import hashlib
import socket
import msgpack
import logging

from pybrew.server import repo


logger = logging.getLogger("brew_server")
SHA256_DIGEST_SIZE = 32


class MetricsRecorder(object):
    def __init__(self, config):
        self.host, self.port = config['endpoint'].split(':')
        self.port = int(self.port)
        self.hmac_key = str(config['hmac_key'].decode('base64'))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ipaddr = socket.gethostbyname(self.host)
        self.repo = repo.MetricsRepo(config['db'])

    @staticmethod
    def _hmac_valid(sig1, sig2):
        valid = True
        for (a, b) in zip(sig1, sig2):
            if a != b:
                valid = False

        return valid and len(sig1) == len(sig2)

    def _parse_payload(self, payload):
        signature = payload[:SHA256_DIGEST_SIZE]
        data = payload[SHA256_DIGEST_SIZE:]

        expected_sig = hmac.new(self.hmac_key, data, hashlib.sha256).digest()

        valid = self._hmac_valid(signature, expected_sig)
        if not valid:
            raise Exception("Signature does not match")

        (key, value) = msgpack.unpackb(data)
        return (key, value)

    def _bind(self):
        self.sock.bind((self.host, self.port))

    def run(self):
        self._bind()

        while True:
            try:
                logger.info("Waiting for next payload")
                self._process_next_payload()
            except Exception as e:
                logger.error("Error saving payload", exc_info=True)
                if isinstance(e, KeyboardInterrupt):
                    raise

    def _store_key_value(self, key, value):
        self.repo.store_metric(unicode(key), unicode(value))

    def _process_next_payload(self):
        (data, addr) = self.sock.recvfrom(512)
        logger.info("Received data from %s", addr)
        if not data:
            return

        len_data = data[:4]
        if len(len_data) != 4:
            logger.error("Unknown data received %s",
                         len_data.encode('hex'))
            return

        (payload_len, ) = struct.unpack('!L', len_data)
        logger.info("Recieved length %d", payload_len)

        payload = data[4:]
        if len(payload) != payload_len:
            logger.error("Bad Payload length %d", len(payload))
            return

        logger.info("Recieved Payload")

        (key, value) = self._parse_payload(payload)
        self._store_key_value(key, value)
