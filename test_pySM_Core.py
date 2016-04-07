import random
import logging

from unittest import TestCase

from core import PySM_Core

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('tests')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)

class TestPySM_Core(TestCase):
    def test_EAX(self):
        LOG.debug("Testing EAX registers ...")

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

        core.EAX = 4294967295
        self.assertEqual(core.EAX, 4294967295)
        self.assertEqual(core.AX, 65535)
        self.assertEqual(core.AH, 255)
        self.assertEqual(core.AL, 255)


    def test_EBX(self):
        LOG.debug("Testing EBX registers ...")

        core = PySM_Core()

        self.assertEqual(core.EBX, 0)

        core.EBX = 42
        self.assertEqual(core.EBX, 42)
        self.assertEqual(core.BX, 42)
        self.assertEqual(core.BH, 0)
        self.assertEqual(core.BL, 42)

        core.BH = 1
        self.assertEqual(core.EBX, 298)
        self.assertEqual(core.BX, 298)
        self.assertEqual(core.BH, 1)
        self.assertEqual(core.BL, 42)

        core.BL += 1
        self.assertEqual(core.EBX, 299)
        self.assertEqual(core.BX, 299)
        self.assertEqual(core.BH, 1)
        self.assertEqual(core.BL, 43)

        core.BX = 543
        self.assertEqual(core.EBX, 543)
        self.assertEqual(core.BX, 543)
        self.assertEqual(core.BH, 2)
        self.assertEqual(core.BL, 31)

        core.BX = 0
        self.assertEqual(core.EBX, 0)
        self.assertEqual(core.BX, 0)
        self.assertEqual(core.BH, 0)
        self.assertEqual(core.BL, 0)

        core.EBX = 4294967295
        self.assertEqual(core.EBX, 4294967295)
        self.assertEqual(core.BX, 65535)
        self.assertEqual(core.BH, 255)
        self.assertEqual(core.BL, 255)


    def test_ECX(self):
        LOG.debug("Testing ECX registers ...")

        core = PySM_Core()

        self.assertEqual(core.ECX, 0)

        core.ECX = 42
        self.assertEqual(core.ECX, 42)
        self.assertEqual(core.CX, 42)
        self.assertEqual(core.CH, 0)
        self.assertEqual(core.CL, 42)

        core.CH = 1
        self.assertEqual(core.ECX, 298)
        self.assertEqual(core.CX, 298)
        self.assertEqual(core.CH, 1)
        self.assertEqual(core.CL, 42)

        core.CL += 1
        self.assertEqual(core.ECX, 299)
        self.assertEqual(core.CX, 299)
        self.assertEqual(core.CH, 1)
        self.assertEqual(core.CL, 43)

        core.CX = 543
        self.assertEqual(core.ECX, 543)
        self.assertEqual(core.CX, 543)
        self.assertEqual(core.CH, 2)
        self.assertEqual(core.CL, 31)

        core.ECX = 0
        self.assertEqual(core.ECX, 0)
        self.assertEqual(core.CX, 0)
        self.assertEqual(core.CH, 0)
        self.assertEqual(core.CL, 0)

        core.ECX = 4294967295
        self.assertEqual(core.ECX, 4294967295)
        self.assertEqual(core.CX, 65535)
        self.assertEqual(core.CH, 255)
        self.assertEqual(core.CL, 255)


    def test_EDX(self):
        LOG.debug("Testing EDX registers ...")

        core = PySM_Core()

        self.assertEqual(core.EDX, 0)

        core.EDX = 42
        self.assertEqual(core.EDX, 42)
        self.assertEqual(core.DX, 42)
        self.assertEqual(core.DH, 0)
        self.assertEqual(core.DL, 42)

        core.DH = 1
        self.assertEqual(core.EDX, 298)
        self.assertEqual(core.DX, 298)
        self.assertEqual(core.DH, 1)
        self.assertEqual(core.DL, 42)

        core.DL += 1
        self.assertEqual(core.EDX, 299)
        self.assertEqual(core.DX, 299)
        self.assertEqual(core.DH, 1)
        self.assertEqual(core.DL, 43)

        core.DX = 543
        self.assertEqual(core.EDX, 543)
        self.assertEqual(core.DX, 543)
        self.assertEqual(core.DH, 2)
        self.assertEqual(core.DL, 31)

        core.DX = 0
        self.assertEqual(core.EDX, 0)
        self.assertEqual(core.DX, 0)
        self.assertEqual(core.DH, 0)
        self.assertEqual(core.DL, 0)

        core.EDX = 4294967295
        self.assertEqual(core.EDX, 4294967295)
        self.assertEqual(core.DX, 65535)
        self.assertEqual(core.DH, 255)
        self.assertEqual(core.DL, 255)

    def test_set_memory_location(self):
        LOG.debug("Testing memory access ...")
        core = PySM_Core()

        core.set_memory_location(0, 0)
        self.assertEqual(core.get_memory_location(0), 0)

        core.set_memory_location(0xffff, 0xff)
        self.assertEqual(core.get_memory_location(0xffff), 0xff)

        core.set_memory_location(0x10000, 0xff)
        self.assertEqual(core.get_memory_location(0x00), 0xff)


        for run in range(1000):
            offset = random.randint(0x00,0xffffff)
            value = random.randint(0x00, 0xffff)
            core.set_memory_location(offset, value)
            self.assertEqual(core.get_memory_location(offset & 0xffff), value & 0xff)

        # for l in core.dump_memory():
        #     LOG.debug(l)

    def test_add_ptr(self):
        LOG.debug("Testing symbol management ...")
        core = PySM_Core()

        #msg = [ord(c) for c in "Hello World!"]
        #msg.append(0x00)
        #LOG.debug("message: {}".format(msg))
        for i in range(10):
            ptr_name = "ptr_{}".format(i)
            msg = [ord(c) for c in "Hello World #{}!".format(i)]
            msg.append(0x00)

            core.add_pointer(ptr_name)
            core.set_pointer_value(ptr_name, core.malloc(len(msg)))
            core.set_memory_range(core.get_poointer_value(ptr_name), msg)
            for l in core.dump_memory(limit=0x0005):
                LOG.debug(l)

        ptr_name = 'ptr_2'
        core.free(core.get_poointer_value(ptr_name))
        core.delete_pointer(ptr_name)
        for l in core.dump_memory(limit=0x0005):
            LOG.debug(l)

        ptr_name = 'ptr_4'
        core.free(core.get_poointer_value(ptr_name))
        core.delete_pointer(ptr_name)
        for l in core.dump_memory(limit=0x0005):
            LOG.debug(l)

        ptr_name = 'ptr_6'
        core.free(core.get_poointer_value(ptr_name))
        core.delete_pointer(ptr_name)
        for l in core.dump_memory(limit=0x0005):
            LOG.debug(l)

        ptr_name = "ptr_{}_n".format(1)
        msg = [ord(c) for c in "Hello!".upper()]
        msg.append(0x00)
        core.add_pointer(ptr_name)
        core.set_pointer_value(ptr_name, core.malloc(len(msg)))
        core.set_memory_range(core.get_poointer_value(ptr_name), msg)
        for l in core.dump_memory(limit=0x0005):
            LOG.debug(l)

        ptr_name = "ptr_{}_n".format(2)
        msg = [ord(c) for c in "World!".format(i).upper()]
        msg.append(0x00)
        core.add_pointer(ptr_name)
        core.set_pointer_value(ptr_name, core.malloc(len(msg)))
        core.set_memory_range(core.get_poointer_value(ptr_name), msg)
        for l in core.dump_memory(limit=0x0005):
            LOG.debug(l)

            # for i in range(10):
        #     ptr_name = "ptr_{}".format(i)
        #     core.free(core.get_poointer_value(ptr_name))
        #     core.delete_pointer(ptr_name)



