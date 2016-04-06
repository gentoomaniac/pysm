from unittest import TestCase

from core import PySM_Core

class TestPySM_Core(TestCase):
    def test_EAX(self):
        core = PySM_Core()

        self.assertEqual(core.EAX, 0)

        core.EAX = 42
        self.assertEqual(core.EAX, 42)
        self.assertEqual(core.AX, 42)
        self.assertEqual(core.AH, 0)
        self.assertEqual(core.AL, 42)

        core.AH = 1
        self.assertEqual(core.EAX, 298)
        self.assertEqual(core.AX, 298)
        self.assertEqual(core.AH, 1)
        self.assertEqual(core.AL, 42)

        core.AL += 1
        self.assertEqual(core.EAX, 299)
        self.assertEqual(core.AX, 299)
        self.assertEqual(core.AH, 1)
        self.assertEqual(core.AL, 43)

        core.AX = 543
        self.assertEqual(core.EAX, 543)
        self.assertEqual(core.AX, 543)
        self.assertEqual(core.AH, 2)
        self.assertEqual(core.AL, 31)

        core.AX = 0
        self.assertEqual(core.EAX, 0)
        self.assertEqual(core.AX, 0)
        self.assertEqual(core.AH, 0)
        self.assertEqual(core.AL, 0)

        core.EAX = 2147483647
        self.assertEqual(core.EAX, 2147483647)
        self.assertEqual(core.AX, 65535)
        self.assertEqual(core.AH, 255)
        self.assertEqual(core.AL, 255)
