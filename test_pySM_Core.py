import random
import logging

from unittest import TestCase

from core import PySM_Core

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('t_memory')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)

class TestPySM_Core(TestCase):

    def test_set_memory_location(self):
        LOG.debug("Testing memory access ...")
        core = PySM_Core()

        core.set_memory_location(0, 0)
        self.assertEqual(core.get_memory_location(0), 0)

        core.set_memory_location(0xffff, 0xff)
        self.assertEqual(core.get_memory_location(0xffff), 0xff)

        core.set_memory_location(0x10000, 0xff)
        self.assertEqual(core.get_memory_location(0x00), 0xff)


        for run in range(100000):
            offset = random.randint(0x00,0xffffff)
            value = random.randint(0x00, 0xffff)
            core.set_memory_location(offset, value)
            self.assertEqual(core.get_memory_location(offset & 0xffff), value & 0xff)

        for l in core.dump_memory():
            LOG.debug(l)

    def test_add_ptr(self):
        LOG.debug("Testing malloc() ...")
        core = PySM_Core()

        ptr_name = "ptr_1"
        core.add_pointer(ptr_name)
        core.set_pointer_value(ptr_name, core.malloc(16))
        self.assertEqual(core.get_pointer_value(ptr_name), 0x00)

        ptr_name = "ptr_2"
        core.add_pointer(ptr_name)
        core.set_pointer_value(ptr_name, core.malloc(16))
        self.assertEqual(core.get_pointer_value(ptr_name), 0x10)

        ptr_name = "ptr_3"
        core.add_pointer(ptr_name)
        core.set_pointer_value(ptr_name, core.malloc(16))
        self.assertEqual(core.get_pointer_value(ptr_name), 0x20)

        ptr_name = "ptr_4"
        core.add_pointer(ptr_name)
        core.set_pointer_value(ptr_name, core.malloc(16))
        self.assertEqual(core.get_pointer_value(ptr_name), 0x30)

        ptr_name = "ptr_5"
        core.add_pointer(ptr_name)
        core.set_pointer_value(ptr_name, core.malloc(16))
        self.assertEqual(core.get_pointer_value(ptr_name), 0x40)

        ptr_name = 'ptr_2'
        core.free(core.get_pointer_value(ptr_name))
        core.delete_pointer(ptr_name)

        ptr_name = "ptr_1_n"
        core.add_pointer(ptr_name)
        core.set_pointer_value(ptr_name, core.malloc(7))
        self.assertEqual(core.get_pointer_value(ptr_name), 0x10)

        ptr_name = "ptr_2_n"
        core.add_pointer(ptr_name)
        core.set_pointer_value(ptr_name, core.malloc(6))
        self.assertEqual(core.get_pointer_value(ptr_name), 0x17)

        ptr_name = "ptr_3_n"
        core.add_pointer(ptr_name)
        core.set_pointer_value(ptr_name, core.malloc(6))
        self.assertEqual(core.get_pointer_value(ptr_name), 0x50)
        for l in core.dump_memory(limit=0x0006):
            LOG.debug(l)


    # def test_set_mem_range(self):
    #     LOG.debug("Testing set_memory_range() ...")
    #     core = PySM_Core()
    #
    #     for i in range(6):
    #         ptr_name = "ptr_{}".format(i)
    #         msg = [ord(c) for c in "Hello World #{}!".format(i)]
    #         msg.append(0x00)
    #
    #         core.add_pointer(ptr_name)
    #         core.set_pointer_value(ptr_name, core.malloc(len(msg)))
    #         core.set_memory_range(core.get_pointer_value(ptr_name), msg)
    #         for l in core.dump_memory(limit=0x0006):
    #             LOG.debug(l)
    #
    #     ptr_name = 'ptr_2'
    #     core.free(core.get_pointer_value(ptr_name))
    #     core.delete_pointer(ptr_name)
    #     for l in core.dump_memory(limit=0x0006):
    #         LOG.debug(l)
    #
    #     ptr_name = "ptr_{}_n".format(1)
    #     msg = [ord(c) for c in "Hello!".upper()]
    #     msg.append(0x00)
    #     core.add_pointer(ptr_name)
    #     core.set_pointer_value(ptr_name, core.malloc(len(msg)))
    #     core.set_memory_range(core.get_pointer_value(ptr_name), msg)
    #     for l in core.dump_memory(limit=0x0006):
    #         LOG.debug(l)
    #
    #     ptr_name = "ptr_{}_n".format(2)
    #     msg = [ord(c) for c in "World!123".format(i).upper()]
    #     msg.append(0x00)
    #     core.add_pointer(ptr_name)
    #     core.set_pointer_value(ptr_name, core.malloc(len(msg)))
    #     core.set_memory_range(core.get_pointer_value(ptr_name), msg)
    #     for l in core.dump_memory(limit=0x007):
    #         LOG.debug(l)
    #
    #         # for i in range(10):
    #         #     ptr_name = "ptr_{}".format(i)
    #         #     core.free(core.get_pointer_value(ptr_name))
    #         #     core.delete_pointer(ptr_name)
    #
    #
    #
