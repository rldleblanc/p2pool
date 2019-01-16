import unittest
import hashlib
import random

from p2pool.bitcoin import sha256

class Test(unittest.TestCase):
    def test_all(self):
        for test in [b'', b'a', b'b', b'abc', b'abc'*50, b'hello world']:
            #print test
            #print sha256.sha256(test).hexdigest()
            #print hashlib.sha256(test).hexdigest()
            #print
            assert sha256.sha256(test).hexdigest() \
                    == hashlib.sha256(test).hexdigest().encode('ascii')
        def random_str(l):
            return bytes((random.randrange(256) for i in range(l)))
        for length in range(150):
            test = random_str(length)
            a = sha256.sha256(test).hexdigest()
            b = hashlib.sha256(test).hexdigest().encode('ascii')
            assert a == b
        for i in range(100):
            test = random_str(int(random.expovariate(1/100)))
            test2 = random_str(int(random.expovariate(1/100)))

            a = sha256.sha256(test)
            a = a.copy()
            a.update(test2)
            a = a.hexdigest()

            b = hashlib.sha256(test)
            b = b.copy()
            b.update(test2)
            b = b.hexdigest().encode('ascii')
            assert a == b
