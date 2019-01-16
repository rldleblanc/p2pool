import unittest
import random

from p2pool.util import pack
from p2pool.bitcoin.data import (FloatingInteger, FloatingIntegerType,
                                 TransactionType, ChecksummedType)

class Test(unittest.TestCase):
    def test_VarInt(self):
        t = pack.VarIntType()
        for i in range(2**20):
            assert t.unpack(t.pack(i)) == i
        for i in range(2**36, 2**36+25):
            assert t.unpack(t.pack(i)) == i

    def test_Int(self):
        for endianness in ['little', 'big']:
            off = 0
            for size in [8, 16, 32, 64, 128, 192, 256]:
                t = pack.IntType(size, endianness)
                num = off
                off += 1
                if size < 16:
                    step = 1
                else:
                    # Test 8K values
                    step = (1 << size) //  (1 << 13)
                cnt = 0
                while num < (1 << size):
                    self.assertEqual(num, t.unpack(t.pack(num)))
                    num += step
                    cnt += 1

    def test_VarStr(self):
        t = pack.VarStrType()
        msg = b''
        for i in range(260):
            self.assertEqual(msg, t.unpack(t.pack(msg)))
            msg += bytes([random.randint(40, 126)])


    def test_Enum(self):
        values = {}
        for i in range(16):
            values[i] = ''.join([chr(random.randint(40, 126))
                for x in range(random.randint(1, 10))])
            t = pack.EnumType(pack.VarIntType(), values)
            for q in range(i+1):
                self.assertEqual(values[q], t.unpack(t.pack(values[q])))

    def test_List(self):
        values = []
        t = pack.ListType(pack.IntType(32))
        for i in range(260):
            self.assertListEqual(values, t.unpack(t.pack(values)))
            values.append(random.randint(0, (1 << 32) - 1))

    def test_Struct(self):
        for endian in ('<', '>'):
            for bits, fmt in ((8, 'B'), (16, 'H'), (32, 'I'), (64, 'Q')):
                t = pack.StructType('%s%s' % (endian, fmt))
                for err in [-2, -1, 1 << bits, (1 << bits) + 1]:
                    # raises a generic 'error' and not sure where from.
                    self.assertRaises(Exception, t.pack, err)
                for good in [0, 1, 2, 1 << (bits // 2), (1 << bits) - 2,
                             (1 << bits) - 1]:
                    self.assertEqual(good, t.unpack(t.pack(good)))

    def test_IPV6Address(self):
        t = pack.IPV6AddressType()
        ipv4addr = '192.168.21.18'
        self.assertEqual(ipv4addr, t.unpack(t.pack(ipv4addr)))
        # Does not support compact addresses
        ipv6addr = 'dead:beef:0123:4567:89ab:cdef:fedc:0001'
        self.assertEqual(ipv6addr, t.unpack(t.pack(ipv6addr)))


    def test_Composed(self):
        t = pack.ComposedType([('one', pack.IntType(8)),
                               ('two', pack.VarStrType())])
        values = {'one': 1, 'two': b'2'}
        self.assertDictEqual(values, dict(t.unpack(t.pack(values))))
        values = {'one': b'1', 'two': 2}
        # Another generic error
        self.assertRaises(Exception, t.pack, values)

    def test_PossiblyNone(self):
        for i in range(1 << 8):
            t = pack.PossiblyNoneType(i, pack.IntType(8))
            self.assertEqual(None, t.unpack(t.pack(None)))
            for q in range(1 << 8):
                if q == i:
                    self.assertRaises(ValueError, t.pack, q)
                    continue
                self.assertEqual(q, t.unpack(t.pack(q)))

    def test_FixedStr(self):
        value = ''.join([chr(random.randint(40, 126)) for x in range(270)])
        value = value.encode('ascii')
        for i in range(260):
            t = pack.FixedStrType(i)
            for q in range(i -2, i + 2):
                if q < 0:
                    continue
                if q == i:
                    self.assertEqual(value[:q], t.unpack(t.pack(value[:q])))
                    continue
                self.assertRaises(ValueError, t.pack, value[:q])

    # These are in p2pool.bitcoin.data

    def test_FloatingInteger_value(self):
        x = b'!\x00\x80\x00'
        res = 'FloatingInteger(bits=0x21008000, target=0x8000000000000000000000000000000000000000000000000000000000000000)'
        y = FloatingIntegerType().unpack(x[::-1])
        self.assertEqual(res, str(y))
        z = FloatingInteger(int.from_bytes(x, 'big'))
        self.assertEqual(y, z)

    def test_FloatingInteger(self):
        val = FloatingInteger(1)
        t = FloatingIntegerType()
        self.assertEqual(val, t.unpack(t.pack(val)))
        val = FloatingInteger((1 << 10) - 1)
        self.assertEqual(val, t.unpack(t.pack(val)))
        val = FloatingInteger((1 << 30) - 1)
        self.assertEqual(val, t.unpack(t.pack(val)))

    def test_Transaction(self):
        t = TransactionType()
        tx_ins = [{'previous_output': None, 'script': b'In script',
                   'sequence': None}]
        tx_outs = [{'value': 8, 'script': b'hello!'}]
        data = {'version': 1, 'tx_ins': tx_ins, 'tx_outs': tx_outs,
                'lock_time': 0}
        self.assertDictEqual(data, t.unpack(t.pack(data)))
        witness = [[b'Witness data']]
        data['marker'] = 0
        data['flag'] = 1
        data['witness'] = witness
        self.assertDictEqual(data, t.unpack(t.pack(data)))

    def test_Checksummed(self):
        t = ChecksummedType(pack.VarStrType())
        self.assertEqual(b'foobar', t.unpack(t.pack(b'foobar')))
        value = {'version': 1, 'pubkey_hash': 1234567890}
        t = ChecksummedType(pack.ComposedType([('version', pack.IntType(8)),
                                               ('pubkey_hash', pack.IntType(160))]))
        self.assertDictEqual(value, dict(t.unpack(t.pack(value))))
