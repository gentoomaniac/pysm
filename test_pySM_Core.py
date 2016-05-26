import random
import logging

from unittest import TestCase

import stdlib
from core import Core
import datatypes.exceptions as exceptions

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('t_memory')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)


class TestPySM_Core(TestCase):
    def test_set_memory_location(self):
        LOG.debug("Testing memory access ...")
        core = Core()

        core.set_memory_location(0, 0)
        self.assertEqual(core.get_memory_location(0), 0)

        core.set_memory_location(0xffff, 0xff)
        self.assertEqual(core.get_memory_location(0xffff), 0xff)

        core.set_memory_location(0x10000, 0xff)
        self.assertEqual(core.get_memory_location(0x00), 0xff)

        for run in range(100000):
            offset = random.randint(0x00, 0xffffff)
            value = random.randint(0x00, 0xffff)
            core.set_memory_location(offset, value)
            self.assertEqual(core.get_memory_location(offset & 0xffff), value & 0xff)

        for l in core.dump_memory():
            LOG.debug(l)

    def test_set_mem_range(self):
        LOG.debug("Testing set_memory_range() ...")

        core = Core()
        mem_locations = {}

        for i in range(6):
            ptr_name = "ptr_{}".format(i)
            msg = [ord(c) for c in "Hello World #{}!".format(i)]
            msg.append(0x00)

            mem_locations[ptr_name] = stdlib.malloc(len(msg))
            core.set_memory_range(mem_locations[ptr_name], msg)
            for l in core.dump_memory(limit=0x0006):
                LOG.debug(l)

        stdlib.free(mem_locations.pop('ptr_2'))
        for l in core.dump_memory(limit=0x0006):
            LOG.debug(l)

        ptr_name = "ptr_{}_n".format(1)
        msg = [ord(c) for c in "Hello!".upper()]
        msg.append(0x00)
        mem_locations[ptr_name] = stdlib.malloc(len(msg))
        core.set_memory_range(mem_locations[ptr_name], msg)
        for l in core.dump_memory(limit=0x0006):
            LOG.debug(l)

        ptr_name = "ptr_{}_n".format(2)
        msg = [ord(c) for c in "World!123".format(i).upper()]
        msg.append(0x00)
        mem_locations[ptr_name] = stdlib.malloc(len(msg))
        core.set_memory_range(mem_locations[ptr_name], msg)
        for l in core.dump_memory(limit=0x007):
            LOG.debug(l)

    def test_inc(self):
        LOG.debug("Testing inc() ...")
        core = Core()

        core.EAX = 0xffffffff

        core.inc("EAX")
        self.assertEqual(core.EAX, 0)
        self.assertGreater(core.EFLAGS & 0x01, 0)

    def test_dec(self):
        LOG.debug("Testing dec() ...")
        core = Core()

        core.EAX = 0xffffffff
        core.dec("EAX")
        self.assertEqual(core.EAX, 0xfffffffe)

        core.EAX = 0x00000001
        core.dec("EAX")
        self.assertEqual(core.EAX, 0x00000000)

        core.EAX = 0x00000000
        core.dec("EAX")
        self.assertEqual(core.EAX, 0xffffffff)
        self.assertGreater(core.EFLAGS & 0x01, 0)

    def test_mov(self):
        LOG.debug("Testing mov() ...")
        core = Core()

        core.mov("EAX", 0xff)
        self.assertEqual(core.EAX, 0xff)

        core.mov("EBX", "EAX")
        self.assertEqual(core.EBX, 0xff)

        core.mov("CH", "EAX")
        self.assertEqual(core.CH, 0xff)

    def test_push_pop(self):
        LOG.debug("Testing stack functions ...")
        core = Core()

        core.dump_stack()

        LOG.debug("Pushing 0xff from EBX to stack")
        core.EBX = 0xff
        core.push("EBX")
        core.dump_stack()

        LOG.debug("Pushing 0xf0 as integer to stack")
        core.push(0xf0)
        core.dump_stack()

        LOG.debug("pop() into EAX")
        core.pop("EAX")
        self.assertEqual(core.EAX, 0xf0)
        core.dump_stack()

        LOG.debug("pop() into ECX")
        core.pop("ECX")
        self.assertEqual(core.ECX, 0xff)
        core.dump_stack()

        core.push(0x666)
        core.dump_stack()
        core.pop()
        core.dump_stack()

        # LOG.debug("pop() into EDX to provoke exception")
        # self.assertRaises(IndexError, core.pop("EDX"))

    def test_sys_write(self):
        LOG.debug("Testing sys_write() ...")
        core = Core()

        msg = [ord(c) for c in "Hello!"]
        msg.append(0x00)
        addr = stdlib.malloc(len(msg))
        length = len(msg)

        core.set_memory_range(addr, msg)

        core.EAX = 4        # sys_write
        core.EBX = 2        # stderr
        core.ECX = addr
        core.EDX = length

        core.interrupt(0x80)      # handover to core

        stdlib.free(addr)
