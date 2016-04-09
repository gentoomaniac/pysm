import collections
import json
import logging
import string

import register as r


FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('core')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)

class PySM_Core(object):

    def __init__(self):
        # memory
        self._mem = [int(0)] * (0xffff+1)

        # registers
        self._EAX = r.Register()
        self._EBX = r.Register()
        self._ECX = r.Register()
        self._EDX = r.Register()

        self._EIP = r.Register()
        self._ESP = r.Register()
        self._EBP = r.Register()

        self._ESI = r.Register()
        self._EDI = r.Register()

        # special stuff
        self._IP = 0        # instruction pointer
        self._EFLAGS = 0    # Flags register

        # some management tables

        self._memtab = {}
        self._pointer = {}

    def inc(self, target):
        if target in self._pointer:
            LOG.debug("Incrementing memory location at {:04X} referenced by {}".format(self._pointer[target], target))
            value = self.get_memory_location(self._pointer[target])
            self.set_memory_location(self._pointer[target], value + 1)
            self._set_co_bit(value, value + 1, 0xff)
        elif isinstance(target, int):
            LOG.debug("Incrementing memory location {:04X}".format(target & 0xffff))
            address = target & 0xffff
            value = self.get_memory_location(address)
            self.set_memory_location(address, value + 1)
            self._set_co_bit(value, value + 1, 0xff)
        elif hasattr(self, target.upper()):
            LOG.debug("Incrementing register {}".format(target.upper()))
            value = getattr(self, target.upper())
            setattr(self, target.upper(), value + 1)
            self._set_co_bit(value, value + 1, 0xff) ### TODO: how to figure out which size the register had?
        else:
            raise ValueError("Invalid ADD parameter")

    def _set_co_bit(self, old_value, new_value, max):
        # set overflow flag
        if old_value > ( new_value & max):
            self._EFLAGS | 0x01

    def _mallof_find_free(self, size):
        last_addr = 0x00
        current_addr = None
        is_end = True

        # transform dict to flat list
        memtab = collections.OrderedDict(sorted(self._memtab.items())).items()
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

    def malloc(self, size):
        address = self._mallof_find_free(size)
        if address is None:
            raise Exception("Couldn't allocate memory")

        self._memtab[address] = address + size-1
        LOG.debug("Allocated {} bytes at address {:04X}".format(size, address))
        LOG.debug("Memory allocation table: {}".format(json.dumps(self._memtab, sort_keys=True)))
        return address

    def free(self, address):
        if address in self._memtab:
            LOG.debug("Freed {} bytes at address {:04X}".format(address, address))
            self._memtab.pop(address)
        LOG.debug("Memory allocation table: {}".format(json.dumps(self._memtab, sort_keys=True)))

    def add_pointer(self, name, value=0x00):
        if name in self._pointer:
            raise ValueError("{} already exists".format(name))
        LOG.debug("Adding new pointer '{}' with value {:04X}".format(name, value))
        self._pointer[name] = value & 0xffff
        LOG.debug("Pointer table: {}".format(json.dumps(self._pointer, sort_keys=True)))

    def delete_pointer(self, name):
        if name in self._pointer:
            LOG.debug("Removed pointer '{}' with value {:04X}".format(name, self._pointer[name]))
            self._pointer.pop(name)
        LOG.debug("Pointer table: {}".format(json.dumps(self._pointer, sort_keys=True)))

    def get_pointer_value(self, name):
            return self._pointer.get(name, None)

    def set_pointer_value(self, name, value):
        if name not in self._pointer:
            raise ValueError("{} does not exist".format(name))
        self._pointer[name] = value & 0xffff

    def set_memory_range(self, address, values):
        for v in values:
            self.set_memory_location(address, v)
            address += 1

    def set_memory_location(self, offset, value):
        if not isinstance(offset, int) or not isinstance(value, int):
            raise ValueError("Address or value must be integers")
        offset &= 0xffff
        value &= 0xff
        self._mem[offset] = value
        #LOG.debug("memory at address {:04X} is set to {:02X}".format(offset, self._mem[offset]))

    def get_memory_location(self, offset):
        if not isinstance(offset, int):
           raise ValueError("Address must be an integer")
        offset &= 0xffff
        return self._mem[offset]

    def dump_memory(self, limit=0xffff):
        result = []
        count = 1
        rowcount = 0
        line = "{:04X}h: ".format(rowcount*0x0f)
        text = ""
        for byte in self._mem:
            line += "{:02X} ".format(int(byte))
            if chr(byte) in string.whitespace or byte == 0x00:
                text += '.'
            else:
                text += chr(byte)

            if (count % 0x10) == 0:
                line += "    {}".format(text)
                result.append(line)
                rowcount += 1
                line = "{:04X}h: ".format(rowcount*0x10)
                text = ""

            if rowcount >= limit:
                break
            count += 1

        return result

    def dump_registers(self):
        return """
        EAX: {:32b}
        EBX: {:32b}
        ECX: {:32b}
        EDX: {:32b}
        """.format(self._EAX.full, self._EBX.full, self._ECX.full, self._EDX.full)

    @property
    def EAX(self):
        """ primary accumulator (32Bit)
        it is used in input/output and most arithmetic instructions. For example, in multiplication operation,
        one operand is stored in EAX or AX or AL register according to the size of the operand
        """
        return self._EAX.full

    @EAX.setter
    def EAX(self, value):
        self._EAX.full = value
        LOG.debug("EAX is now {}".format(self.EAX))

    @property
    def AX(self):
        return self._EAX.half

    @AX.setter
    def AX(self, value):
        self._EAX.half = value
        LOG.debug("AX is now {}".format(self.AX))

    @property
    def AH(self):
        return self._EAX.high

    @AH.setter
    def AH(self, value):
        self._EAX.high = value
        LOG.debug("AH is now {}".format(self.AH))

    @property
    def AL(self):
        return self._EAX.low

    @AL.setter
    def AL(self, value):
        self._EAX.low = value
        LOG.debug("AL is now {}".format(self.AL))


    @property
    def EBX(self):
        """ base register (32Bit)
        used in indexed addressing
        """
        return self._EBX.full

    @EBX.setter
    def EBX(self, value):
        self._EBX.full = value
        LOG.debug("EBX is now {}".format(self.EBX))

    @property
    def BX(self):
        return self._EBX.half

    @BX.setter
    def BX(self, value):
        self._EBX.half = value
        LOG.debug("BX is now {}".format(self.BX))

    @property
    def BH(self):
        return self._EBX.high

    @BH.setter
    def BH(self, value):
        self._EBX.high = value
        LOG.debug("BH is now {}".format(self.BH))

    @property
    def BL(self):
        return self._EBX.low

    @BL.setter
    def BL(self, value):
        self._EBX.low = value
        LOG.debug("BL is now {}".format(self.BL))


    @property
    def ECX(self):
        """ count register (32Bit)
        stores the loop count in iterative operations
        """
        return self._ECX.full

    @ECX.setter
    def ECX(self, value):
        self._ECX.full = value
        LOG.debug("ECX is now {}".format(self.ECX))

    @property
    def CX(self):
        return self._ECX.half

    @CX.setter
    def CX(self, value):
        self._ECX.half = value
        LOG.debug("CX is now {}".format(self.CX))

    @property
    def CH(self):
        return self._ECX.high

    @CH.setter
    def CH(self, value):
        self._ECX.high = value
        LOG.debug("CH is now {}".format(self.CH))

    @property
    def CL(self):
        return self._ECX.low

    @CL.setter
    def CL(self, value):
        self._ECX.low = value
        LOG.debug("CL is now {}".format(self.CL))


    @property
    def EDX(self):
        """ data register (32Bit)
        It is also used in input/output operations.
        It is also used with AX register along with DX for multiply and divide operations involving large values.
        """
        return self._EDX.full

    @EDX.setter
    def EDX(self, value):
        self._EDX.full = value
        LOG.debug("EDX is now {}".format(self.EDX))

    @property
    def DX(self):
        return self._EDX.half

    @DX.setter
    def DX(self, value):
        self._EDX.half = value
        LOG.debug("DX is now {}".format(self.DX))

    @property
    def DH(self):
        return self._EDX.high

    @DH.setter
    def DH(self, value):
        self._EDX.high = value
        LOG.debug("DH is now {}".format(self.DH))

    @property
    def DL(self):
        return self._EDX.low

    @DL.setter
    def DL(self, value):
        self._EDX.low = value
        LOG.debug("DL is now {}".format(self.DL))
