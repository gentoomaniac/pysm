import collections
import logging
import json

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('stdlib')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)

_memtab = {}


def malloc(size):
    address = _malloc_find_free(size)
    if address is None:
        raise Exception("Couldn't allocate memory")

    _memtab[address] = address + size - 1
    LOG.debug("Allocated {} bytes at address {:04X}".format(size, address))
    LOG.debug("Memory allocation table: {}".format(json.dumps(_memtab, sort_keys=True)))
    return address


def _malloc_find_free(size):
    last_addr = 0x00
    current_addr = None
    is_end = True

    # transform dict to flat list
    memtab = collections.OrderedDict(sorted(_memtab.items())).items()
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

def free(address):
    if address in _memtab:
        LOG.debug("Freed {} bytes at address {:04X}".format(address, address))
        _memtab.pop(address)
    LOG.debug("Memory allocation table: {}".format(json.dumps(_memtab, sort_keys=True)))

def sizeof(obj):
    try:
        return obj.size
    except:
        raise AttributeError("Object doesn't have a size")
