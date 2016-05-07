import logging
from unittest import TestCase

import datatypes.exceptions as exceptions
from datatypes.word import Word

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('test_word')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)

class TestWord(TestCase):

    def test_value(self):
        LOG.info("Testing complete word ...")
        w = Word()

        self.assertEqual(w.value, 0x0000)

        w.value = 0x000f
        self.assertEqual(w.value, 0x000f)

        w.value = 0x00ff
        self.assertEqual(w.value, 0x00ff)

        w.value = 0x0100
        self.assertEqual(w.value, 0x0100)

        w.value = 0xffff
        self.assertEqual(w.value, 0xffff)

        try:
            w.value = 0x010000
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.value, 0x0000)

        try:
            w.value = 0x010001
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.value, 0x0001)

    def test_high(self):
        LOG.info("Testing high Byte ...")
        w = Word()

        self.assertEqual(w.high.value, 0x00)

        w.high.value = 0x0f
        self.assertEqual(w.high.value, 0x0f)

        w.high.value = 0xff
        self.assertEqual(w.high.value, 0xff)

        try:
            w.high.value = 0x0100
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.high.value, 0x00)

        try:
            w.high.value = 0x010f
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.high.value, 0x0f)

    def test_low(self):
        LOG.info("Testing low Byte ...")
        w = Word()

        self.assertEqual(w.low.value, 0x00)

        w.low.value = 0x0f
        self.assertEqual(w.low.value, 0x0f)

        w.low.value = 0xff
        self.assertEqual(w.low.value, 0xff)

        try:
            w.low.value = 0x0100
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.low.value, 0x00)

        try:
            w.low.value = 0x010f
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(w.low.value, 0x0f)

    def test_size(self):
        LOG.info("Testing size ...")
        w = Word()
        self.assertEqual(w.size, 16)
