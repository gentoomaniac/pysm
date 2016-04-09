import logging
from unittest import TestCase

import datatypes.exceptions as exceptions
from datatypes.dword import Dword

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('test_dword')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)

class TestDword(TestCase):

    def test_value(self):
        LOG.info("Testing complete dword ...")
        w = Dword()

        self.assertEqual(w.value, 0x00000000)

        w.value = 0x0000000f
        self.assertEqual(w.value, 0x0000000f)

        w.value = 0x000000ff
        self.assertEqual(w.value, 0x000000ff)

        w.value = 0x00000100
        self.assertEqual(w.value, 0x00000100)

        w.value = 0x0000ffff
        self.assertEqual(w.value, 0x0000ffff)

        w.value = 0x00ffffff
        self.assertEqual(w.value, 0x00ffffff)

        w.value = 0xffffffff
        self.assertEqual(w.value, 0xffffffff)

        try:
            w.value = 0x0100000000
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.value, 0x00000000)

        try:
            w.value = 0x0100000001
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.value, 0x00000001)

    def test_high(self):
        LOG.info("Testing high Byte ...")
        w = Dword()

        self.assertEqual(w.high.value, 0x0000)

        w.high.value = 0x000f
        self.assertEqual(w.high.value, 0x000f)

        w.high.value = 0x00ff
        self.assertEqual(w.high.value, 0x00ff)

        w.high.value = 0x0fff
        self.assertEqual(w.high.value, 0x0fff)

        w.high.value = 0xffff
        self.assertEqual(w.high.value, 0xffff)

        try:
            w.high.value = 0x010000
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.high.value, 0x0000)

        try:
            w.high.value = 0x01000f
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.high.value, 0x000f)

    def test_low(self):
        LOG.info("Testing low Byte ...")
        w = Dword()

        self.assertEqual(w.low.value, 0x0000)

        w.low.value = 0x000f
        self.assertEqual(w.low.value, 0x000f)

        w.low.value = 0x00ff
        self.assertEqual(w.low.value, 0x00ff)

        w.low.value = 0x0fff
        self.assertEqual(w.low.value, 0x0fff)

        w.low.value = 0xffff
        self.assertEqual(w.low.value, 0xffff)

        try:
            w.low.value = 0x010000
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.low.value, 0x0000)

        try:
            w.low.value = 0x01000f
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.low.value, 0x000f)
