import binascii
import struct
from io import BytesIO
import os

import p2pool
from p2pool.util import memoize

class EarlyEnd(Exception):

    __slots__ = ()

    pass

class LateEnd(Exception):

    __slots__ = ()

    pass

def remaining(sio):
    here = sio.tell()
    sio.seek(0, os.SEEK_END)
    end  = sio.tell()
    sio.seek(here)
    return end - here

class Type(object):

    __slots__ = ()

    def __hash__(self):
        rval = getattr(self, '_hash', None)
        if rval is None:
            try:
                rval = self._hash = hash(
                        (type(self), frozenset(self.__dict__.items())))
            except:
                print(self.__dict__)
                raise
        return rval

    def __eq__(self, other):
        return type(other) is type(self) and other.__dict__ == self.__dict__

    def __ne__(self, other):
        return not (self == other)

    def _unpack(self, data, ignore_trailing=False):
        obj = self.read(data)
        if not ignore_trailing and remaining(data):
            raise LateEnd()
        return obj

    def _pack(self, obj):
        f = BytesIO()
        self.write(f, obj)
        return f.getvalue()

    def unpack(self, data, ignore_trailing=False):
        if not isinstance(data, BytesIO):
            data = BytesIO(data)
        obj = self._unpack(data, ignore_trailing)

        if p2pool.DEBUG:
            packed = self._pack(obj)
            good = data.getvalue().startswith(packed) if \
                    ignore_trailing else data.getvalue() == packed
            if not good:
                raise AssertionError(ignore_trailing, packed, data.getvalue())

        return obj

    def pack(self, obj):
        # No check since obj can have more keys than our type
        return self._pack(obj)

    def packed_size(self, obj):
        if hasattr(obj, '_packed_size') and obj._packed_size is not None:
            type_obj, packed_size = obj._packed_size
            if type_obj is self:
                return packed_size

        packed_size = len(self.pack(obj))

        if hasattr(obj, '_packed_size'):
            obj._packed_size = self, packed_size

        return packed_size

class VarIntType(Type):

    __slots__ = ()

    def read(self, file):
        data = file.read(1)
        first = ord(data)
        if first < 0xfd:
            return first
        if first == 0xfd:
            desc, length, minimum = '<H', 2, 0xfd
        elif first == 0xfe:
            desc, length, minimum = '<I', 4, 2**16
        elif first == 0xff:
            desc, length, minimum = '<Q', 8, 2**32
        else:
            raise AssertionError()
        data2 = file.read(length)
        res, = struct.unpack(desc, data2)
        if res < minimum:
            raise AssertionError('VarInt not canonically packed')
        return res

    def write(self, file, item):
        if item < 0xfd:
            return file.write(struct.pack('<B', item))
        elif item <= 0xffff:
            return file.write(struct.pack('<BH', 0xfd, item))
        elif item <= 0xffffffff:
            return file.write(struct.pack('<BI', 0xfe, item))
        elif item <= 0xffffffffffffffff:
            return file.write(struct.pack('<BQ', 0xff, item))
        else:
            raise ValueError('int too large for varint')

class VarStrType(Type):

    __slots__ = ()

    _inner_size = VarIntType()

    def read(self, file):
        length = self._inner_size.read(file)
        return file.read(length)

    def write(self, file, item):
        if not isinstance(item, (bytes, bytearray)):
            raise ValueError("Can only pack a string in bytes() or bytearray().")
        self._inner_size.write(file, len(item))
        file.write(item)

class EnumType(Type):

    __slots__ = ('inner', 'pack_to_unpack', 'unpack_to_pack')

    def __init__(self, inner, pack_to_unpack):
        self.inner = inner
        self.pack_to_unpack = pack_to_unpack

        self.unpack_to_pack = {}
        for k, v in pack_to_unpack.items():
            if v in self.unpack_to_pack:
                raise ValueError('duplicate value in pack_to_unpack')
            self.unpack_to_pack[v] = k

    def read(self, file):
        data = self.inner.read(file)
        if data not in self.pack_to_unpack:
            raise ValueError('enum data (%r) not in pack_to_unpack (%r)' % (
                data, self.pack_to_unpack))
        return self.pack_to_unpack[data]

    def write(self, file, item):
        if item not in self.unpack_to_pack:
            raise ValueError('enum item (%r) not in unpack_to_pack (%r)' % (
                item, self.unpack_to_pack))
        self.inner.write(file, self.unpack_to_pack[item])

class ListType(Type):

    __slots__ = ('type', 'mul')

    _inner_size = VarIntType()

    def __init__(self, type, mul=1):
        self.type = type
        self.mul = mul

    def read(self, file):
        length = self._inner_size.read(file)
        length *= self.mul
        res = [self.type.read(file) for i in range(length)]
        return res

    def write(self, file, item):
        assert len(item) % self.mul == 0
        self._inner_size.write(file, len(item)//self.mul)
        for subitem in item:
            self.type.write(file, subitem)

class StructType(Type):

    __slots__ = ('desc', 'length')

    def __init__(self, desc):
        self.desc = desc
        self.length = struct.calcsize(self.desc)

    def read(self, file):
        data = file.read(self.length)
        return struct.unpack(self.desc, data)[0]

    def write(self, file, item):
        file.write(struct.pack(self.desc, item))

@memoize.fast_memoize_multiple_args
class IntType(Type):

    __slots__ = ('bytes', 'step', 'format_str', 'max')

    def __new__(cls, bits, endianness='little'):
        assert bits % 8 == 0
        assert endianness in ['little', 'big']
        if bits in [8, 16, 32, 64]:
            return StructType(('<' if endianness == 'little' else '>') +
                    {8: 'B', 16: 'H', 32: 'I', 64: 'Q'}[bits])
        else:
            return super(cls, cls).__new__(cls)

    def __init__(self, bits, endianness='little'):
        assert bits % 8 == 0
        assert endianness in ['little', 'big']
        self.bytes = bits // 8
        self.step = -1 if endianness == 'little' else 1
        self.format_str = b'%%0%ix' % (2 * self.bytes)
        self.max = 2**bits

    def read(self, file, hexlify=binascii.hexlify):
        if self.bytes == 0:
            return 0
        data = file.read(self.bytes)
        return int(hexlify(data[::self.step]), 16)

    def write(self, file, item, unhexlify=binascii.unhexlify):
        if self.bytes == 0:
            return None
        if not 0 <= item < self.max:
            raise ValueError('invalid int value - %r' % item)
        file.write(unhexlify(self.format_str % item)[::self.step])

class IPV6AddressType(Type):

    __slots__ = ()

    def read(self, file):
        data = file.read(16)
        if data[:12] == binascii.unhexlify('00000000000000000000ffff'):
            return '.'.join(str(int(x)) for x in data[12:])
        return ':'.join(binascii.hexlify(data[i*2:(i+1)*2]).decode('ascii') for
                i in range(8))

    def write(self, file, item):
        if ':' in item:
            data = binascii.unhexlify(''.join(item.replace(':', '')))
        else:
            bits = bytes([int(x) for x in item.split('.')])
            if len(bits) != 4:
                raise ValueError('invalid address: %r' % bits)
            data = b'%s%s' % (binascii.unhexlify('00000000000000000000ffff'),
                    bits)
        assert len(data) == 16, len(data)
        file.write(data)

_record_types = {}

def get_record(fields):
    fields = tuple(sorted(fields))
    if 'keys' in fields or '_packed_size' in fields:
        raise ValueError()
    if fields not in _record_types:
        class _Record(object):

            __slots__ = fields + ('_packed_size',)

            def __init__(self):
                self._packed_size = None
            def __repr__(self):
                return repr(dict(self))
            def __getitem__(self, key):
                return getattr(self, key)
            def __setitem__(self, key, value):
                setattr(self, key, value)
            #def __iter__(self):
            #    for field in fields:
            #        yield field, getattr(self, field)
            def keys(self):
                return fields
            def get(self, key, default=None):
                return getattr(self, key, default)
            def __eq__(self, other):
                if isinstance(other, dict):
                    return dict(self) == other
                elif isinstance(other, _Record):
                    for k in fields:
                        if getattr(self, k) != getattr(other, k):
                            return False
                    return True
                elif other is None:
                    return False
                raise TypeError()
            def __ne__(self, other):
                return not (self == other)
        _record_types[fields] = _Record
    return _record_types[fields]

class ComposedType(Type):

    __slots__ = ('fields', 'field_names', 'record_type')

    def __init__(self, fields):
        self.fields = list(fields)
        self.field_names = set(k for k, v in fields)
        self.record_type = get_record(k for k, v in self.fields)

    def read(self, file):
        item = self.record_type()
        for key, type_ in self.fields:
            item[key] = type_.read(file)
        return item

    def write(self, file, item):
        assert set(item.keys()) >= self.field_names
        for key, type_ in self.fields:
            type_.write(file, item[key])

class PossiblyNoneType(Type):

    __slots__ = ('none_value', 'inner')

    def __init__(self, none_value, inner):
        self.none_value = none_value
        self.inner = inner

    def read(self, file):
        value = self.inner.read(file)
        return None if value == self.none_value else value

    def write(self, file, item):
        if item == self.none_value:
            raise ValueError('none_value used')
        self.inner.write(file, self.none_value if item is None else item)

class FixedStrType(Type):

    __slots__ = ('length')

    def __init__(self, length):
        self.length = length

    def read(self, file):
        return file.read(self.length)

    def write(self, file, item):
        if len(item) != self.length:
            raise ValueError('incorrect length item!')
        if not isinstance(item, (bytes, bytearray)):
            raise ValueError("Can only pack a string in bytes() or bytearray().")
        file.write(item)
