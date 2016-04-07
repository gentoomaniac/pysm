import collections
import logging
import string


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
        self._EAX = 0
        self._EBX = 0
        self._ECX = 0
        self._EDX = 0

        self._EIP = 0
        self._ESP = 0
        self._EBP = 0

        self._ESI = 0
        self._EDI = 0

        # special stuff
        self._IP = 0        # instruction pointer
        self._EFLAGS = 0    # Flags register

        # some management tables

        self._memtab = {}
        self._pointer = {}

    def _mallof_find_free(self, size):
        last_addr = 0x00
        current_addr = None
        is_end = True

        # transform dict to flat list
        memtab = collections.OrderedDict(sorted(self._memtab.items())).items()
        memtab = [i for s in memtab for i in s]


        # no memory reserved
        if not memtab:
            LOG.debug("Memtab is empty. Giving 0x00.")
            return 0x00

        # check the amount of from the ending of the last block to the next block
        for addr in memtab:
            is_end = not is_end
            current_addr = addr
            if not is_end:
                LOG.debug("Checking start address: {:04X} - {:04X}".format(addr, last_addr))
                if (addr - last_addr) >= size:
                    LOG.debug("Found address: {:04X}".format(last_addr))
                    return last_addr

            last_addr = addr

        if is_end and (0xffff - current_addr >= size):
            LOG.debug("current address is {} and we have enough space".format(current_addr))
            return current_addr

        return None

    def malloc(self, size):
        address = self._mallof_find_free(size)
        if address is None:
            raise Exception("Couldn't allocate memory")

        self._memtab[address] = address + size
        LOG.debug("Allocated {} bytes at address {:04X}".format(size, address))
        LOG.debug("Memory allocation table: {}".format(self._memtab))
        return address

    def free(self, address):
        if address in self._memtab:
            LOG.debug("Freed {} bytes at address {:04X}".format(address, address))
            self._memtab.pop(address)
        LOG.debug("Memory allocation table: {}".format(self._memtab))

    def add_pointer(self, name, value=0x00):
        if name in self._pointer:
            raise ValueError("{} already exists".format(name))
        LOG.debug("Adding new pointer '{}' with value {:04X}".format(name, value))
        self._pointer[name] = value & 0xffff
        LOG.debug("Pointer table: {}".format(self._pointer))

    def delete_pointer(self, name):
        if name in self._pointer:
            LOG.debug("Removed pointer '{}' with value {:04X}".format(name, self._pointer[name]))
            self._pointer.pop(name)
        LOG.debug("Pointer table: {}".format(self._pointer))

    def get_poointer_value(self, name):
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

        return result #[re.sub(r"[\t\n\r]", " ", r) for r in result]

    def dump_registers(self):
        return """
        EAX: {:32b}
        EBX: {:32b}
        ECX: {:32b}
        EDX: {:32b}
        """.format(self._EAX, self._EBX, self._ECX, self._EDX)

    @property
    def EAX(self):
        """ primary accumulator (32Bit)
        it is used in input/output and most arithmetic instructions. For example, in multiplication operation,
        one operand is stored in EAX or AX or AL register according to the size of the operand
        """
        return self._EAX & 0xffffffff

    @EAX.setter
    def EAX(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._EAX = value & 0xffffffff
        LOG.debug("EAX is now {}".format(self.EAX))

    @property
    def AX(self):
        return self._EAX & 0xffff

    @AX.setter
    def AX(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._EAX = (self._EAX | 0x0000ffff) & ((value & 0xffff) | 0xffff0000)
        LOG.debug("AX is now {}".format(self.AX))

    @property
    def AH(self):
        return (self._EAX & 0xff00) >> 8

    @AH.setter
    def AH(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        limited_value = value & 0xff                # limit the value to 8 bits
        shifted_value = limited_value << 8          # shift those bits to the right position
        masked_value = shifted_value | 0xffff00ff   # mask the bits we don't want to update

        eax_masked = self._EAX | 0x0000ff00         # mask out the bits we want to update
        #LOG.debug("EAX:        {0:32b}".format(self._EAX))
        #LOG.debug("eax_masked: {0:32b}".format(eax_masked))
        #LOG.debug("value:      {0:32b}".format(value))
        #LOG.debug("value lim:  {0:32b}".format(limited_value))
        #LOG.debug("value shift:{0:32b}".format(shifted_value))
        #LOG.debug("value mask: {0:32b}".format(masked_value))
        #LOG.debug("AND:        {0:32b}".format(masked_value & eax_masked))
        self._EAX = masked_value & eax_masked       # merge the two masks into one new updated register
        LOG.debug("AH is now {}".format(self.AH))

    @property
    def AL(self):
        return self._EAX & 0xff

    @AL.setter
    def AL(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._EAX = (self._EAX | 0x000000ff) & ((value & 0xff) | 0xffffff00)
        LOG.debug("AL is now {}".format(self.AL))


    @property
    def EBX(self):
        """ base register (32Bit)
        used in indexed addressing
        """
        return self._EBX & 0xffffffff

    @EBX.setter
    def EBX(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._EBX = value & 0xffffffff
        LOG.debug("EBX is now {}".format(self.EBX))

    @property
    def BX(self):
        return self._EBX & 0xffff

    @BX.setter
    def BX(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._EBX = (self._EBX | 0x0000ffff) & ((value & 0xffff) | 0xffff0000)
        LOG.debug("BX is now {}".format(self.BX))

    @property
    def BH(self):
        return (self._EBX & 0xff00) >> 8

    @BH.setter
    def BH(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        limited_value = value & 0xff  # limit the value to 8 bits
        shifted_value = limited_value << 8  # shift those bits to the right position
        masked_value = shifted_value | 0xffff00ff  # mask the bits we don't want to update

        masked = self._EBX | 0x0000ff00  # mask out the bits we want to update
        self._EBX = masked_value & masked  # merge the two masks into one new updated register
        LOG.debug("BH is now {}".format(self.BH))

    @property
    def BL(self):
        return self._EBX & 0xff

    @BL.setter
    def BL(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._EBX = (self._EBX | 0x000000ff) & ((value & 0xff) | 0xffffff00)
        LOG.debug("BL is now {}".format(self.BL))


    @property
    def ECX(self):
        """ count register (32Bit)
        stores the loop count in iterative operations
        """
        return self._ECX & 0xffffffff

    @ECX.setter
    def ECX(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._ECX = value & 0xffffffff
        LOG.debug("ECX is now {}".format(self.ECX))

    @property
    def CX(self):
        return self._ECX & 0xffff

    @CX.setter
    def CX(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._ECX = (self._ECX | 0x0000ffff) & ((value & 0xffff) | 0xffff0000)
        LOG.debug("CX is now {}".format(self.CX))

    @property
    def CH(self):
        return (self._ECX & 0xff00) >> 8

    @CH.setter
    def CH(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        limited_value = value & 0xff  # limit the value to 8 bits
        shifted_value = limited_value << 8  # shift those bits to the right position
        masked_value = shifted_value | 0xffff00ff  # mask the bits we don't want to update

        masked = self._ECX | 0x0000ff00  # mask out the bits we want to update
        self._ECX = masked_value & masked  # merge the two masks into one new updated register
        LOG.debug("CH is now {}".format(self.CH))

    @property
    def CL(self):
        return self._ECX & 0xff

    @CL.setter
    def CL(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._ECX = (self._ECX | 0x000000ff) & ((value & 0xff) | 0xffffff00)
        LOG.debug("CL is now {}".format(self.CL))


    @property
    def EDX(self):
        """ data register (32Bit)
        It is also used in input/output operations.
        It is also used with AX register along with DX for multiply and divide operations involving large values.
        """
        return self._EDX & 0xffffffff

    @EDX.setter
    def EDX(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._EDX = value & 0xffffffff
        LOG.debug("EDX is now {}".format(self.EDX))

    @property
    def DX(self):
        return self._EDX & 0xffff

    @DX.setter
    def DX(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._EDX = (self._EDX | 0x0000ffff) & ((value & 0xffff) | 0xffff0000)
        LOG.debug("DX is now {}".format(self.DX))

    @property
    def DH(self):
        return (self._EDX & 0xff00) >> 8

    @DH.setter
    def DH(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        limited_value = value & 0xff  # limit the value to 8 bits
        shifted_value = limited_value << 8  # shift those bits to the right position
        masked_value = shifted_value | 0xffff00ff  # mask the bits we don't want to update

        masked = self._EDX | 0x0000ff00  # mask out the bits we want to update
        self._EDX = masked_value & masked  # merge the two masks into one new updated register
        LOG.debug("DH is now {}".format(self.DH))

    @property
    def DL(self):
        return self._EDX & 0xff

    @DL.setter
    def DL(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self._EDX = (self._EDX | 0x000000ff) & ((value & 0xff) | 0xffffff00)
        LOG.debug("DL is now {}".format(self.DL))
