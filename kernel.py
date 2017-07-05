import collections
import core
import logging
import json

from singleton import Singleton

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('kernel')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)

class Kernel(metaclass=Singleton):

    def __init__(self):
        self.__core = core.Core()
        self.__memtab = {}

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
