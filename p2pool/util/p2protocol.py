'''
Generic message-based protocol used by Bitcoin and P2Pool for P2P communication
'''

import hashlib
import struct
import binascii

from twisted.internet import protocol
from twisted.python import log

import p2pool
import p2pool.bitcoin.data as bitcoin_data
from p2pool.util import datachunker, variable

class TooLong(Exception):

    __slots__ = ()

    pass

class Protocol(protocol.Protocol):

    __slots__ = ('_message_prefix', '_max_payload_length', 'dataReceived2',
                 'traffic_happened', 'ignore_trailing_payload')

    def __init__(self, message_prefix, max_payload_length, traffic_happened=variable.Event(), ignore_trailing_payload=False):
        self._message_prefix = message_prefix
        self._max_payload_length = max_payload_length
        self.dataReceived2 = datachunker.DataChunker(self.dataReceiver())
        self.traffic_happened = traffic_happened
        self.ignore_trailing_payload = ignore_trailing_payload

    def dataReceived(self, data):
        self.traffic_happened.happened('p2p/in', len(data))
        self.dataReceived2(data)

    def dataReceiver(self):
        while True:
            start = b''
            while start != self._message_prefix:
                start = (start + (yield 1))[-len(self._message_prefix):]

            command = (yield 12).rstrip(b'\0').decode('ascii')
            length, = struct.unpack('<I', (yield 4))
            if length > self._max_payload_length:
                print('length too large')
                continue
            checksum = yield 4
            payload = yield length

            payload_hash = bitcoin_data.hash256d(payload)
            if payload_hash[:4] != checksum:
                print('invalid hash for %s %s %s %s' % (
                    self.transport.getPeer().host, repr(command), length,
                    checksum.encode('hex')))
                if p2pool.DEBUG:
                    print("%s %s" % (
                        payload_hash[:4].encode('hex'), payload.encode('hex')))
                self.badPeerHappened()
                continue

            type_ = getattr(self, 'message_' + command, None)
            if type_ is None:
                if p2pool.DEBUG:
                    print('no type for %s' % repr(command))
                continue

            try:
                self.packetReceived(command, type_.unpack(
                    payload, self.ignore_trailing_payload))
            except:
                print('RECV %s %s%s' % (
                    command, binascii.hexlify(payload[:100]),
                    '...' if len(payload) > 100 else ''))
                log.err(None, 'Error handling message: (see RECV line)')
                self.disconnect()

    def packetReceived(self, command, payload2):
        handler = getattr(self, 'handle_' + command, None)
        if handler is None:
            if p2pool.DEBUG:
                print('no handler for %s' % repr(command))
            return

        if getattr(self, 'connected', True) and not \
                getattr(self, 'disconnecting', False):
            handler(**payload2)

    def disconnect(self):
        if hasattr(self.transport, 'abortConnection'):
            # Available since Twisted 11.1
            self.transport.abortConnection()
        else:
            # This doesn't always close timed out connections! warned about in main
            self.transport.loseConnection()

    def badPeerHappened(self):
        self.disconnect()

    def sendPacket(self, command, payload2):
        if len(command) >= 12:
            raise ValueError('command too long')
        type_ = getattr(self, 'message_' + command, None)
        if type_ is None:
            raise ValueError('invalid command')
        #print 'SEND', command, repr(payload2)[:500]
        payload = type_.pack(payload2)
        if len(payload) > self._max_payload_length:
            raise TooLong('payload too long')
        data = self._message_prefix + struct.pack(
                '<12sI', command.encode('ascii'), len(payload)) + hashlib.sha256(
                        hashlib.sha256(payload).digest()).digest()[:4] + payload
        self.traffic_happened.happened('p2p/out', len(data))
        self.transport.write(data)

    def __getattr__(self, attr):
        prefix = 'send_'
        if attr.startswith(prefix):
            command = attr[len(prefix):]
            return lambda **payload2: self.sendPacket(command, payload2)
        #return protocol.Protocol.__getattr__(self, attr)
        raise AttributeError(attr)
