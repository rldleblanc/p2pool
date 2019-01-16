# Copyright (c) 2017 Pieter Wuille
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Reference implementation for Bech32 and segwit addresses."""

from p2pool.util.math import convertbits

CHARSET = b"qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def bech32_polymod(values):
    """Internal function that computes the Bech32 checksum.

    Args:
        values: The data as a list of integers to compute checksum over.

    Returns:
        the checksum value as an int.
    """
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk

def bech32_hrp_expand(hrp):
    """Expand the HRP into values for checksum computation.

    Args:
        hrp: The human readable part in bytes().

    Returns:
        A list of integer values.
    """
    return [x >> 5 for x in hrp] + [0] + [x & 31 for x in hrp]

def bech32_verify_checksum(hrp, data):
    """Verify a checksum given HRP and converted data characters.

    Args:
        hrp: The human readable part in bytes().
        data: The data as a list of integers.

    Ruturns:
        True if valid, False if invalid.
    """
    return bech32_polymod(bech32_hrp_expand(hrp) + data) == 1

def bech32_create_checksum(hrp, data):
    """Compute the checksum values given HRP and data.

    Args:
        hrp: The human readable part as bytes().
        data: The address data as a list of integers.

    Returns:
        The checksum as a list of integers.
    """
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

def bech32_encode(hrp, data):
    """Compute a Bech32 string given HRP and data values.

    Args:
        hrp: The human readable part in bytes().
        data: The data as a list of integers.

    Returns:
        A Bech32 address in bytes().
    """
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + b'1' + bytes([CHARSET[d] for d in combined])

def bech32_decode(bech):
    """Validate a Bech32 string, and determine HRP and data.

    Args:
        bech: The Bech32 address as bytes().

    Returns:
        Tuple with the human readable part and the data as an int.
    """
    if ((any(x < 33 or x > 126 for x in bech)) or
            (bech.lower() != bech and bech.upper() != bech)):
        return (None, None)
    bech = bech.lower()
    pos = bech.rfind(b'1')
    if pos < 1 or pos + 7 > len(bech) or len(bech) > 90:
        return (None, None)
    if not all(x in CHARSET for x in bech[pos+1:]):
        return (None, None)
    hrp = bech[:pos]
    data = [CHARSET.find(x) for x in bech[pos+1:]]
    if not bech32_verify_checksum(hrp, data):
        return (None, None)
    return (hrp, data[:-6])

def decode(hrp, addr):
    """Decode a segwit address.

    Args:
        hrp: The human readable part as bytes().
        addr: The Bech32 as bytes().

    Returns:
        A tuple of version and the payload data as a list of integers.
    """
    hrpgot, data = bech32_decode(addr)
    if hrpgot != hrp:
        return (None, None)
    decoded = convertbits(data[1:], 5, 8, False)
    if decoded is None or len(decoded) < 2 or len(decoded) > 40:
        return (None, None)
    if data[0] > 16:
        return (None, None)
    if data[0] == 0 and len(decoded) != 20 and len(decoded) != 32:
        return (None, None)
    return (data[0], decoded)

def encode(hrp, witver, witprog):
    """Encode a segwit address.

    Args:
        hrp: The human readable part as bytes().
        witver: An integer representing the segwit version.
        witprog: The witness data as a list of integers.

    Returns:
        A Bech32 address as bytes().
    """
    ret = bech32_encode(hrp, [witver] + convertbits(witprog, 8, 5))
    if decode(hrp, ret) == (None, None):
        return None
    return ret
