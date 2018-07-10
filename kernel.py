import collections
import logging
import json

from core import Core
from singleton import Singleton

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('kernel')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)


class Kernel(metaclass=Singleton):

    def __init__(self, core=Core(), screen=None):
        self.__core = core
        self.__screen = screen
        self.__memtab = {}


        # https://filippo.io/linux-syscall-table/
        # some management tables
        self._syscalls = {
            0x01: self.sys_exit,
            0x04: self.sys_write
        }

    def interrupt(self, num):
        LOG.debug("Interrupt received: {}".format(num))
        if num == 0x80:
            LOG.debug("Executing syscall: {}".format(self.__core.EAX))
            self._syscalls[self.__core.EAX]()

    def sys_exit(self):
        LOG.debug("sys_exit() ...")

    def sys_write(self):
        LOG.debug("Printing to screen ...")
        msg_addr = self.__core.ECX
        msg_len = self.__core.EDX
        msg_target = self.__core.EBX

        msg = self.__core.get_memory_range(msg_addr, msg_len)

        if msg_target == 1:
            if not self.__screen:
                raise IOError("No screen connected!")
            x=0
            for c in msg:
                self.__screen.set_character(c, x, 0, 10)
                x += 1
            self.__screen.update_screen_buffer()
        elif msg_target == 2:
            msg = [chr(c) for c in msg]
            LOG.error("".join(msg))
        else:
            raise ValueError("sys_write() can only write to stdout or stderr")

    def allocate_memory(self, size):
        LOG.debug("Memory allocation table: {}".format(json.dumps(self.__memtab, sort_keys=True)))
        address = self.__find_free_memory(size)
        if not address is None:
            self.__memtab[address] = address + size - 1
            LOG.debug("Memory allocation table: {}".format(json.dumps(self.__memtab, sort_keys=True)))
        return address

    def __find_free_memory(self, size):
        last_addr = 0x00
        current_addr = None
        is_end = True

        # transform dict to flat list
        memtab = collections.OrderedDict(sorted(self.__memtab.items())).items()
        memtab = [i for s in memtab for i in s]

        # no memory reserved
        if not memtab:
            return 0x00

        # check the amount of from the ending of the last block to the next block
        for addr in memtab:
            is_end = not is_end
            current_addr = addr
            if not is_end:
                if (addr - last_addr) > size:
                    return last_addr + 1

            last_addr = addr

        if is_end and (0xffff - current_addr > size):
            return current_addr + 1

        return None

    def free_memory(self, address):
        if address in self.__memtab:
            LOG.debug("Freed {} bytes at address {:04X}".format(self.__memtab[address], address))
            self.__memtab.pop(address)
        LOG.debug("Memory allocation table: {}".format(json.dumps(self.__memtab, sort_keys=True)))
