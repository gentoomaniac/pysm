import kernel
import logging

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('stdlib')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)

def malloc(size):
    address = kernel.Kernel().allocate_memory(size)
    if address is None:
        raise Exception("Couldn't allocate memory")

    LOG.debug("Allocated {} bytes at address {:04X}".format(size, address))
    return address

def free(address):
    kernel.Kernel().free_memory(address)

def sizeof(obj):
    try:
        return obj.size
    except:
        raise AttributeError("Object doesn't have a size")
