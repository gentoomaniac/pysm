import sys

from unittest import TestCase

import datatypes.exceptions as exceptions
from datatypes.byte import Byte


class TestByte(TestCase):
    def test_value(self):
        b = Byte()

        self.assertEqual(b.value, 0x00)

        b.value = 0x0f
        self.assertEqual(b.value, 0x0f)

        b.value = 0xff
        self.assertEqual(b.value, 0xff)

        try:
            b.value = 0x0100
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(b.value, 0x00)

        try:
            b.value = 0x010f
        except Exception as e:
            self.assertIsInstance(e, exceptions.CarryOverException)
        self.assertEqual(b.value, 0x0f)

        self.assertEqual(b.size, 8)
