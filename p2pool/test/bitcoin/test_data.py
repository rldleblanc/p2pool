import unittest
import mock

from p2pool.bitcoin import data, networks
from p2pool.util import pack


class Test(unittest.TestCase):
    def test_header_hash(self):
        assert data.hash256(data.block_header_type.pack(dict(
            version=1,
            previous_block=0x000000000000038a2a86b72387f93c51298298a732079b3b686df3603d2f6282,
            merkle_root=0x37a43a3b812e4eb665975f46393b4360008824aab180f27d642de8c28073bc44,
            timestamp=1323752685,
            bits=data.FloatingInteger(437159528),
            nonce=3658685446,
        ))) == 0x000000000000003aaaf7638f9f9c0d0c60e8b0eb817dcdb55fd2b1964efc5175
    
    def test_header_hash_litecoin(self):
        assert networks.nets['litecoin'].POW_FUNC(data.block_header_type.pack(dict(
            version=1,
            previous_block=0xd928d3066613d1c9dd424d5810cdd21bfeef3c698977e81ec1640e1084950073,
            merkle_root=0x03f4b646b58a66594a182b02e425e7b3a93c8a52b600aa468f1bc5549f395f16,
            timestamp=1327807194,
            bits=data.FloatingInteger(0x1d01b56f),
            nonce=20736,
        ))) < 2**256//2**30
    
    def test_tx_hash(self):
        assert data.get_txid(dict(
            version=1,
            tx_ins=[dict(
                previous_output=None,
                sequence=None,
                script='70736a0468860e1a0452389500522cfabe6d6d2b2f33cf8f6291b184f1b291d24d82229463fcec239afea0ee34b4bfc622f62401000000000000004d696e656420627920425443204775696c6420ac1eeeed88'.decode('hex'),
            )],
            tx_outs=[dict(
                value=5003880250,
                script=data.pubkey_hash_to_script2(pack.IntType(160).unpack('ca975b00a8c203b8692f5a18d92dc5c2d2ebc57b'.decode('hex')), networks.nets['bitcoin'].ADDRESS_VERSION, -1, networks.nets['bitcoin']),
            )],
            lock_time=0,
        )) == 0xb53802b2333e828d6532059f46ecf6b313a42d79f97925e457fbbfda45367e5c
    
    def test_address_to_pubkey_hash(self):
        assert data.address_to_pubkey_hash('1KUCp7YP5FP8ViRxhfszSUJCTAajK6viGy', networks.nets['bitcoin'])[0] == pack.IntType(160).unpack('ca975b00a8c203b8692f5a18d92dc5c2d2ebc57b'.decode('hex'))
    
    def test_merkle_hash(self):
        assert data.merkle_hash([
            0xb53802b2333e828d6532059f46ecf6b313a42d79f97925e457fbbfda45367e5c,
            0x326dfe222def9cf571af37a511ccda282d83bedcc01dabf8aa2340d342398cf0,
            0x5d2e0541c0f735bac85fa84bfd3367100a3907b939a0c13e558d28c6ffd1aea4,
            0x8443faf58aa0079760750afe7f08b759091118046fe42794d3aca2aa0ff69da2,
            0x4d8d1c65ede6c8eab843212e05c7b380acb82914eef7c7376a214a109dc91b9d,
            0x1d750bc0fa276f89db7e6ed16eb1cf26986795121f67c03712210143b0cb0125,
            0x5179349931d714d3102dfc004400f52ef1fed3b116280187ca85d1d638a80176,
            0xa8b3f6d2d566a9239c9ad9ae2ed5178dee4a11560a8dd1d9b608fd6bf8c1e75,
            0xab4d07cd97f9c0c4129cff332873a44efdcd33bdbfc7574fe094df1d379e772f,
            0xf54a7514b1de8b5d9c2a114d95fba1e694b6e3e4a771fda3f0333515477d685b,
            0x894e972d8a2fc6c486da33469b14137a7f89004ae07b95e63923a3032df32089,
            0x86cdde1704f53fce33ab2d4f5bc40c029782011866d0e07316d695c41e32b1a0,
            0xf7cf4eae5e497be8215778204a86f1db790d9c27fe6a5b9f745df5f3862f8a85,
            0x2e72f7ddf157d64f538ec72562a820e90150e8c54afc4d55e0d6e3dbd8ca50a,
            0x9f27471dfbc6ce3cbfcf1c8b25d44b8d1b9d89ea5255e9d6109e0f9fd662f75c,
            0x995f4c9f78c5b75a0c19f0a32387e9fa75adaa3d62fba041790e06e02ae9d86d,
            0xb11ec2ad2049aa32b4760d458ee9effddf7100d73c4752ea497e54e2c58ba727,
            0xa439f288fbc5a3b08e5ffd2c4e2d87c19ac2d5e4dfc19fabfa33c7416819e1ec,
            0x3aa33f886f1357b4bbe81784ec1cf05873b7c5930ab912ee684cc6e4f06e4c34,
            0xcab9a1213037922d94b6dcd9c567aa132f16360e213c202ee59f16dde3642ac7,
            0xa2d7a3d2715eb6b094946c6e3e46a88acfb37068546cabe40dbf6cd01a625640,
            0x3d02764f24816aaa441a8d472f58e0f8314a70d5b44f8a6f88cc8c7af373b24e,
            0xcc5adf077c969ebd78acebc3eb4416474aff61a828368113d27f72ad823214d0,
            0xf2d8049d1971f02575eb37d3a732d46927b6be59a18f1bd0c7f8ed123e8a58a,
            0x94ffe8d46a1accd797351894f1774995ed7df3982c9a5222765f44d9c3151dbb,
            0x82268fa74a878636261815d4b8b1b01298a8bffc87336c0d6f13ef6f0373f1f0,
            0x73f441f8763dd1869fe5c2e9d298b88dc62dc8c75af709fccb3622a4c69e2d55,
            0xeb78fc63d4ebcdd27ed618fd5025dc61de6575f39b2d98e3be3eb482b210c0a0,
            0x13375a426de15631af9afdf00c490e87cc5aab823c327b9856004d0b198d72db,
            0x67d76a64fa9b6c5d39fde87356282ef507b3dec1eead4b54e739c74e02e81db4,
        ]) == 0x37a43a3b812e4eb665975f46393b4360008824aab180f27d642de8c28073bc44

class UnitTests(unittest.TestCase):

    class btcnet(object):
        SYMBOL = 'btc'
        HUMAN_READABLE_PART = 'bc'
        ADDRESS_VERSION = 0
        ADDRESS_P2SH_VERSION = 3

    class ltcnet(object):
        SYMBOL = 'ltc'
        HUMAN_READABLE_PART = 'ltc'
        ADDRESS_VERSION = 48
        ADDRESS_P2SH_VERSION = 50

    class bchnet(object):
        SYMBOL = 'bch'
        HUMAN_READABLE_PART = 'bitcoincash'
        ADDRESS_VERSION = 0
        ADDRESS_P2SH_VERSION = 3

    @mock.patch.object(data, 'human_address_type', spec=data.human_address_type)
    @mock.patch.object(data, 'base58_encode', spec=data.base58_encode)
    @mock.patch.object(data.segwit_addr, 'encode', spec=data.segwit_addr.encode)
    @mock.patch.object(data.cash_addr, 'encode', spec=data.cash_addr.encode)
    def test_pubkey_hash_to_address(self, mce, mse, mbe, mhat):
        # Test legacy addresses
        mbe.return_value = 'foobar'
        mhat.pack.return_value = 'foo'
        self.assertEqual('foobar',
                         data.pubkey_hash_to_address('bar', 0, 0, self.btcnet))
        self.assertEqual(0, mce.call_count)
        self.assertEqual(0, mse.call_count)
        mbe.assert_called_once_with('foo')
        mhat.pack.assert_called_once_with({'version': 0, 'pubkey_hash': 'bar'})
        mhat.reset_mock()
        self.assertEqual('foobar',
                         data.pubkey_hash_to_address('moo', 1, -1, self.btcnet))
        mhat.pack.assert_called_once_with({'version': 1, 'pubkey_hash': 'moo'})
        # Test segwit addresses
        mse.return_value = 'moobar'
        hash1 = 123486153218641351641531321856105641635163813486135131313818612456474534165
        ret1 = [69, 228, 3, 253, 141, 6, 177, 99, 120, 131, 105, 238, 19, 236,
                234, 73, 29, 205, 107, 201, 9, 238, 81, 64, 21, 78, 5, 81, 3,
                225, 21]
        mhat.reset_mock()
        mbe.reset_mock()
        self.assertEqual('moobar',
                         data.pubkey_hash_to_address(hash1, -1, 0, self.btcnet))
        self.assertEqual(0, mbe.call_count)
        self.assertEqual(0, mhat.call_count)
        self.assertEqual(0, mce.call_count)
        mse.assert_called_once_with('bc', 0, ret1)
        mse.reset_mock()
        hash2 = 4328719365
        ret2 = [1, 2, 3, 4, 5]
        self.assertEqual('moobar',
                         data.pubkey_hash_to_address(hash2, -1, 1, self.ltcnet))
        mse.assert_called_once_with('ltc', 1, ret2)
        # Test cashaddr addresses
        mce.return_value = 'fumbar'
        mse.reset_mock()
        self.assertEqual('fumbar',
                         data.pubkey_hash_to_address(hash1, -1, 0, self.bchnet))
        self.assertEqual(0, mbe.call_count)
        self.assertEqual(0, mhat.call_count)
        self.assertEqual(0, mse.call_count)
        mce.assert_called_once_with('bitcoincash', 0, ret1)
        mce.reset_mock()
        self.assertEqual('fumbar',
                         data.pubkey_hash_to_address(hash2, -1, 1, self.bchnet))
        mce.assert_called_once_with('bitcoincash', 1, ret2)

    @mock.patch.object(data, 'pubkey_hash_to_address',
                       spec=data.pubkey_hash_to_address)
    @mock.patch.object(data, 'hash160', spec=data.hash160)
    def test_pubkey_to_address(self, mh, mphta):
        mphta.return_value = 'foobar'
        mh.return_value = 'foo'
        self.assertEqual('foobar', data.pubkey_to_address('bar', self.btcnet))
        mh.assert_called_once_with('bar')
        mphta.assert_called_once_with('foo', 0, -1, self.btcnet)
        mphta.reset_mock()
        mh.reset_mock()
        self.assertEqual('foobar', data.pubkey_to_address('moo', self.ltcnet))
        mh.assert_called_once_with('moo')
        mphta.assert_called_once_with('foo', 48, -1, self.ltcnet)

    @mock.patch.object(data, 'address_to_pubkey_hash',
                       spec=data.address_to_pubkey_hash)
    @mock.patch.object(data, 'pubkey_hash_to_script2',
                       spec=data.pubkey_hash_to_script2)
    def test_address_to_script2(self, mphts, matph):
        matph.return_value = ('foo', 'moobar', 'meh')
        mphts.return_value = 'bar'
        self.assertEqual('bar', data.address_to_script2('moo', self.btcnet))
        matph.assert_called_once_with('moo', self.btcnet)
        mphts.assert_called_once_with('foo', 'moobar', 'meh', self.btcnet)

    @mock.patch.object(data, 'get_legacy_pubkey_hash',
                       spec=data.get_legacy_pubkey_hash)
    @mock.patch.object(data, 'get_bech32_pubkey_hash',
                       spec=data.get_bech32_pubkey_hash)
    @mock.patch.object(data, 'get_cashaddr_pubkey_hash',
                       spec=data.get_cashaddr_pubkey_hash)
    def test_address_to_pubkey_hash(self, mgcph, mgbph, mglph):
        def reset_mocks():
            for i in mglph, mgbph, mgcph:
                i.reset_mock()

        mglph.return_value = 'legacy'
        mgbph.return_value = 'bech32'
        mgcph.return_value = 'cashaddr'
        self.assertEqual('legacy',
                         data.address_to_pubkey_hash('foo', self.btcnet))
        mglph.assert_called_once_with('foo', self.btcnet)
        reset_mocks()
        mglph.side_effect = [ValueError]
        self.assertRaises(ValueError, data.address_to_pubkey_hash, 'bar',
                          self.ltcnet)
        mglph.assert_called_once_with('bar', self.ltcnet)
        reset_mocks()
        mglph.side_effect = data.AddrError
        self.assertEqual('bech32',
                         data.address_to_pubkey_hash('foo', self.ltcnet))
        mgbph.assert_called_once_with('foo', self.ltcnet)
        reset_mocks()
        self.assertEqual('cashaddr',
                         data.address_to_pubkey_hash('bar', self.bchnet))
        mgcph.assert_called_once_with('bar', self.bchnet)
        reset_mocks()
        mgbph.side_effect = data.AddrError
        self.assertRaises(ValueError, data.address_to_pubkey_hash, 'moo',
                          self.btcnet)
        mgbph.assert_called_once_with('moo', self.btcnet)
        reset_mocks()
        mgcph.side_effect = data.AddrError
        self.assertRaises(ValueError, data.address_to_pubkey_hash, 'foo',
                          self.bchnet)
        mgcph.assert_called_once_with('foo', self.bchnet)

    @mock.patch.object(data, 'base58_decode', spec=data.base58_decode)
    @mock.patch.object(data, 'human_address_type', spec=data.human_address_type)
    def test_get_legacy_pubkey_hash(self, mhat, mbd):
        mbd.side_effect = ValueError
        mhat.unpack.return_value = {'version': 0, 'pubkey_hash': 'foo'}
        self.assertRaises(data.AddrError, data.get_legacy_pubkey_hash, 'bar',
                          self.btcnet)
        mbd.side_effect = None
        mbd.return_value = 'moo'
        mhat.unpack.side_effect = ValueError
        self.assertRaises(data.AddrError, data.get_legacy_pubkey_hash, 'bar',
                          self.btcnet)
        mhat.unpack.side_effect = None
        for t in self.bchnet, self.ltcnet:
            netvers = [t.ADDRESS_VERSION, t.ADDRESS_P2SH_VERSION]
            for v in range(256):
                mbd.reset_mock()
                mhat.reset_mock()
                mhat.unpack.return_value['version'] = v
                if v in netvers:
                    self.assertTupleEqual(('foo', v, -1),
                                          data.get_legacy_pubkey_hash('foobar', t))
                else:
                    self.assertRaises(ValueError, data.get_legacy_pubkey_hash,
                                      'foobar', t)


    @mock.patch.object(data.segwit_addr, 'decode', spec=data.segwit_addr.decode)
    def test_get_bech32_pubkey_hash(self, msd):
        msd.return_value = None, 'bar'
        self.assertRaises(data.AddrError, data.get_bech32_pubkey_hash, 'foo',
                          self.btcnet)
        msd.return_value = 0, None
        self.assertRaises(data.AddrError, data.get_bech32_pubkey_hash, 'foo',
                          self.btcnet)
        msd.side_effect = ValueError
        self.assertRaises(data.AddrError, data.get_bech32_pubkey_hash, 'foo',
                          self.btcnet)
        msd.side_effect = None
        msd.return_value = 3, [1, 2, 3, 4, 5]
        msd.reset_mock()
        self.assertTupleEqual((4328719365, -1, 3),
                              data.get_bech32_pubkey_hash('foo', self.btcnet))
        msd.assert_called_once_with('bc', 'foo')
        msd.reset_mock()
        msd.return_value = 7, [5, 4, 3, 2, 1]
        self.assertTupleEqual((21542142465, -1, 7),
                              data.get_bech32_pubkey_hash('moo', self.ltcnet))
        msd.assert_called_once_with('ltc', 'moo')

    @mock.patch.object(data.cash_addr, 'decode', spec=data.cash_addr.decode)
    def test_get_cashaddr_pubkey_hash(self, mcd):
        mcd.return_value = None, 'bar'
        self.assertRaises(data.AddrError, data.get_cashaddr_pubkey_hash, 'foo',
                          self.bchnet)
        mcd.return_value = 0, None
        self.assertRaises(data.AddrError, data.get_cashaddr_pubkey_hash, 'foo',
                          self.bchnet)
        mcd.side_effect = ValueError
        self.assertRaises(data.AddrError, data.get_cashaddr_pubkey_hash, 'foo',
                          self.bchnet)
        mcd.side_effect = None
        mcd.return_value = 1, [1, 2, 3, 4, 5]
        mcd.reset_mock()
        self.assertTupleEqual((4328719365, -1, 1),
                              data.get_cashaddr_pubkey_hash('foo', self.bchnet))
        mcd.assert_called_once_with('bitcoincash', 'foo')
        mcd.reset_mock()
        mcd.return_value = 7, [5, 4, 3, 2, 1]
        self.assertTupleEqual((21542142465, -1, 7),
                              data.get_cashaddr_pubkey_hash('moo', self.bchnet))
        mcd.assert_called_once_with('bitcoincash', 'moo')

    @mock.patch.object(data, 'pack', spec=data.pack)
    def test_pubkey_hash_to_script2(self, mp):
        mp.IntType().pack.return_value = '\xde\xad\xbe\xef'
        legacy_out = '\x76\xa9\x14\xde\xad\xbe\xef\x88\xac'
        self.assertEqual(legacy_out, data.pubkey_hash_to_script2(1234, 0, -1,
                                                                 self.btcnet))
        mp.IntType().pack.assert_called_once_with(1234)
        mp.reset_mock()
        p2sh_out = '\xa9\x14\xde\xad\xbe\xef\x87'
        self.assertEqual(p2sh_out, data.pubkey_hash_to_script2(1234, 3, -1,
                                                               self.btcnet))
        mp.IntType().pack.assert_called_once_with(1234)
        mp.reset_mock()
        phash = int('deadbeef', 16)
        bech32_out = '\x00\x04\xde\xad\xbe\xef'
        self.assertEqual(bech32_out, data.pubkey_hash_to_script2(phash, -1, 2,
                                                                 self.ltcnet))
        self.assertEqual(0, mp.IntType().pack.call_count)
        cashaddr_out = '\x76\xa9\x04\xde\xad\xbe\xef\x88\xac'
        mp.reset_mock()
        self.assertEqual(cashaddr_out, data.pubkey_hash_to_script2(phash, -1, 1,
                                                                   self.bchnet))
        mp.IntType.assert_called_once_with(32)
        mp.IntType().pack.assert_called_once_with(phash)

        # Max cashaddr hash size.
        phash2 = int('deadbeef' * 16, 16)
        mp.IntType().pack.return_value = '\xde\xad\xbe\xef' * 16
        mp.reset_mock()
        cashaddr_out2 = '\x76\xa9\x40%s\x88\xac' % ('\xde\xad\xbe\xef' * 16)
        self.assertEqual(cashaddr_out2, data.pubkey_hash_to_script2(phash2, -1, 5,
                                                                    self.bchnet))
        mp.IntType.assert_called_once_with(512)
        mp.IntType().pack.assert_called_once_with(phash2)

    @mock.patch.object(data, 'script2_to_pubkey_address',
                       spec=data.script2_to_pubkey_address)
    @mock.patch.object(data, 'script2_to_pubkey_hash_address',
                       spec=data.script2_to_pubkey_hash_address)
    @mock.patch.object(data, 'script2_to_bech32_address',
                       spec=data.script2_to_bech32_address)
    @mock.patch.object(data, 'script2_to_p2sh_address',
                       spec=data.script2_to_p2sh_address)
    def test_script2_to_address(self, mstpa, mstba, mstpha, mstpka):
        mstpa.side_effect = data.AddrError
        mstpa.return_value = 'P2SH'
        mstba.side_effect = data.AddrError
        mstba.return_value = 'Bech32'
        mstpha.side_effect = data.AddrError
        mstpha.return_value = 'Hash'
        mstpka.side_effect = data.AddrError
        mstpka.return_value = 'Pubkey'
        self.assertRaises(ValueError, data.script2_to_address, 'foobar', 1, -1,
                          self.btcnet)
        mstpa.assert_called_once_with('foobar', 1, -1, self.btcnet)
        mstba.assert_called_once_with('foobar', 1, -1, self.btcnet)
        mstpha.assert_called_once_with('foobar', 1, -1, self.btcnet)
        mstpka.assert_called_once_with('foobar', self.btcnet)
        mstpka.side_effect = None
        self.assertEqual('Pubkey', data.script2_to_address('foobar', 1, -1,
                                                            self.btcnet))
        mstpka.side_effect = data.AddrError
        mstpha.side_effect = None
        self.assertEqual('Hash', data.script2_to_address('foobar', 1, -1,
                                                          self.btcnet))
        mstpha.side_effect = data.AddrError
        mstba.side_effect = None
        self.assertEqual('Bech32', data.script2_to_address('foobar', 1, -1,
                                                            self.btcnet))
        mstba.side_effect = data.AddrError
        mstpa.side_effect = None
        self.assertEqual('P2SH', data.script2_to_address('foobar', 1, -1,
                                                          self.btcnet))

    @mock.patch.object(data, 'pubkey_to_script2', spec=data.pubkey_to_script2)
    @mock.patch.object(data, 'pubkey_to_address', spec=data.pubkey_to_address)
    def test_script2_to_pubkey_address(self, mpta, mpts):
        mpts.side_effect = ValueError
        self.assertRaises(data.AddrError, data.script2_to_pubkey_address, 'foo',
                          self.btcnet)
        mpts.side_effect = None
        mpts.return_value = 'moobar'
        mpts.reset_mock()
        self.assertRaises(data.AddrError, data.script2_to_pubkey_address,
                          'foobar', self.btcnet)
        mpts.assert_called_once_with('ooba')
        mpta.return_value = 'foo'
        self.assertEqual('foo', data.script2_to_pubkey_address('moobar',
                                                               self.btcnet))

    @mock.patch.object(data, 'pack', spec=data.pack)
    @mock.patch.object(data, 'pubkey_hash_to_script2',
                       spec=data.pubkey_hash_to_script2)
    @mock.patch.object(data, 'pubkey_hash_to_address',
                       spec=data.pubkey_hash_to_address)
    def test_script2_to_pubkey_hash_address(self, mphta, mphts, mp):
        mp.IntType().unpack.side_effect = ValueError
        mphts.return_value = 'foo'
        self.assertRaises(data.AddrError, data.script2_to_pubkey_hash_address,
                          'bar', 1, -1, self.btcnet)
        mp.IntType().unpack.side_effect = None
        mp.IntType().unpack.return_value = 'moo'
        mphts.side_effect = ValueError
        self.assertRaises(data.AddrError, data.script2_to_pubkey_hash_address,
                          'bar', 1, -1, self.btcnet)
        mphts.side_effect = None
        mp.reset_mock()
        mphts.reset_mock()
        self.assertRaises(data.AddrError, data.script2_to_pubkey_hash_address,
                          'foobar', 1, -1, self.btcnet)
        mp.IntType.assert_called_once_with(160)
        mp.IntType().unpack.assert_called_once_with('b')
        mphts.assert_called_once_with('moo', 1, -1, self.btcnet)
        mphta.return_value = 'moobar'
        self.assertEqual('moobar',
                         data.script2_to_pubkey_hash_address('foo', 1, -1,
                                                             self.btcnet))

    @mock.patch.object(data, 'pubkey_hash_to_script2',
                       spec=data.pubkey_hash_to_script2)
    @mock.patch.object(data, 'pubkey_hash_to_address',
                       spec=data.pubkey_hash_to_address)
    def test_script2_to_bech32_address(self, mphta, mphts):
        phash = '\xde\xad\xbe\xef'
        mphts.side_effect = ValueError
        self.assertRaises(data.AddrError, data.script2_to_bech32_address,
                          phash, 1, -1, self.btcnet)
        mphts.reset_mock()
        mphts.side_effect = None
        mphts.return_value = 'bar'
        self.assertRaises(data.AddrError, data.script2_to_bech32_address,
                          phash, 1, -1, self.btcnet)
        mphts.assert_called_once_with(48879, 1, -1, self.btcnet)
        mphts.return_value = phash
        mphta.return_value = 'foobar'
        self.assertEqual('foobar', data.script2_to_bech32_address(phash, 1, -1,
                                                                  self.btcnet))

    @mock.patch.object(data, 'pack', spec=data.pack)
    @mock.patch.object(data, 'pubkey_hash_to_script2',
                       spec=data.pubkey_hash_to_script2)
    @mock.patch.object(data, 'pubkey_hash_to_address',
                       spec=data.pubkey_hash_to_address)
    def test_script2_to_p2sh_address(self, mphta, mphts, mp):
        mp.IntType().unpack.side_effect = ValueError
        mphts.return_value = 'foo'
        self.assertRaises(data.AddrError, data.script2_to_p2sh_address,
                          'bar', 1, -1, self.btcnet)
        mp.IntType().unpack.side_effect = None
        mp.IntType().unpack.return_value = 'moo'
        mphts.side_effect = ValueError
        self.assertRaises(data.AddrError, data.script2_to_p2sh_address,
                          'bar', 1, -1, self.btcnet)
        mphts.side_effect = None
        mp.IntType().unpack.reset_mock()
        mphts.reset_mock()
        self.assertRaises(data.AddrError, data.script2_to_p2sh_address,
                          'foobar', 1, -1, self.btcnet)
        mp.IntType.called_once_with(160)
        mp.IntType().unpack.assert_called_once_with('oba')
        mphts.assert_called_once_with('moo', 1, -1, self.btcnet)
        mphts.return_value = 'moo'
        mphta.return_value = 'moobar'
        self.assertEqual('moobar', data.script2_to_p2sh_address('moo', 1, -1,
                                                                self.btcnet))

class IntegrationTests(unittest.TestCase):

    btc_addrs = [
                 'bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4',
                 'bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3',
                 '3P14159f73E4gFr7JterCCQh9QjiTjiZrG',
                 '1LR4dmTSS2BV7yrMKKv2SwYBGWhtEGCU29',
                ]

    tbtc_addrs = [
                  'mtXWDB6k5yC5v7TcwKZHB89SUp85yCKshy',
                  '2MzQwSSnBHWHqSAqtTVQ6v47XtaisrJa1Vc',
                  'tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx',
                  'tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7',
                 ]

    ltc_addrs = [
                 'Lf3iRHmfbLcZry4Y28esSJ9ASAfGJtBiyf',
                 'MJVQisa7ragNAvfEMw3Khf5qUDiWQuFtq5',
                 'ltc1q5z36sntfrnd2us8aphw6tmk6ywl49r3q0vk2fm',
                 'ltc1q77e48sy8er43smx84n6ykmxn8p7d7qxdxk5u5xkz98kamlqyrlmsezxv5d',
                ]

    tltc_addrs = [
                  'QfznDEYLScMQokgvUAU8xiGvATevxMfyxy',
                  'tltc1q7jvs3ar80xxexedkrehya6f6jlqqmwdpw8pxrq',
                  'mmkeFSjuEyD5QdnciN4iAHoQuG3rcxnArW',
                 ]

    bch_addrs = [
                 '35qL43qYwLdKtnR7yMfGNDvzv6WyZ8yT2n',
                 'bitcoincash:pqkh9ahfj069qv8l6eysyufazpe4fdjq3u4hna323j',
                 '1D573bqaDiGvMxMRXWoJ6G8yhz9sLs9Z82',
                 'bitcoincash:qzzxswqlwze7c0gj8mwel8l4q3wqk0krlu7jch88gv',
                ]

    bch_addrs2 = [
                  'pqkh9ahfj069qv8l6eysyufazpe4fdjq3u4hna323j',
                  'qzzxswqlwze7c0gj8mwel8l4q3wqk0krlu7jch88gv',
                 ]

    tbch_addrs = [
                  '2MzQwSSnBHWHqSAqtTVQ6v47XtaisrJa1Vc',
                  'mtXWDB6k5yC5v7TcwKZHB89SUp85yCKshy',
                  'bchtest:pp8f7ww2g6y07ypp9r4yendrgyznysc9kqxh6acwu3',
                  'bchtest:qz8tg3hcp86jd7ehqkdr9nuz2hzvks7jmg6lv9mkup',
                  'bchtest:qr2a38zyjmjz7jayf5ne98l3j348e35cw5w49dje2l',
                  'bchtest:pradvyw424yn9a4me27jggcsml47wxznhcp6u5rqak',
                 ]

    tbch_addrs2 = [
                   'pp8f7ww2g6y07ypp9r4yendrgyznysc9kqxh6acwu3',
                   'qz8tg3hcp86jd7ehqkdr9nuz2hzvks7jmg6lv9mkup',
                   'qr2a38zyjmjz7jayf5ne98l3j348e35cw5w49dje2l',
                   'pradvyw424yn9a4me27jggcsml47wxznhcp6u5rqak',
                  ]

    def addr_test(self, addresses, net, prefix=""):
        for addr in addresses:
            script = data.address_to_pubkey_hash(addr, net)
            res = data.pubkey_hash_to_script2(script[0], script[1], script[2], net)
            com_addr = data.script2_to_address(res, script[1], script[2], net)
            self.assertEqual(com_addr, prefix + addr)

    def test_btc_addresses(self):
        self.addr_test(self.btc_addrs, networks.nets['bitcoin'])

    def test_tbtc_addresses(self):
        self.addr_test(self.tbtc_addrs, networks.nets['bitcoin_testnet'])

    def test_ltc_addresses(self):
        self.addr_test(self.ltc_addrs, networks.nets['litecoin'])

    def test_tltc_addresses(self):
        self.addr_test(self.tltc_addrs, networks.nets['litecoin_testnet'])

    def test_bch_addresses(self):
        self.addr_test(self.bch_addrs, networks.nets['bitcoincash'])
        self.addr_test(self.bch_addrs2, networks.nets['bitcoincash'],
                       'bitcoincash:')

    def test_tbch_addresses(self):
        self.addr_test(self.tbch_addrs, networks.nets['bitcoincash_testnet'])
        self.addr_test(self.tbch_addrs2, networks.nets['bitcoincash_testnet'],
                       'bchtest:')
