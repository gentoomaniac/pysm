import logging
import string

import datatypes.exceptions as exceptions
import register as r

from datatypes.byte import *
from datatypes.dword import *

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

        # stack
        self._stack = [int(0)] * (0xff+1)

        # registers
        self._EAX = r.Register32()
        self._EBX = r.Register32()
        self._ECX = r.Register32()
        self._EDX = r.Register32()

        self._EIP = r.Register32()
        self._ESP = r.Register32()
        self._EBP = r.Register32()

        self._ESI = r.Register32()
        self._EDI = r.Register32()

        # special stuff
        self._IP = 0        # instruction pointer
        self._EFLAGS = 0    # Flags register
        self._stack_pointer = -1

        # https://filippo.io/linux-syscall-table/

        # some management tables
        self._opcodes = {

        }

    def push(self, src):
        if isinstance(src, int):
            value = src
        elif hasattr(self, src.upper()):
            value = getattr(self, src.upper())
        else:
            raise TypeError("Invalid value for push()")

        LOG.debug("Pushing {:08X} to stack".format(value))
        try:
            self._stack[self._stack_pointer + 1] = value & 0xffffffff
        except:
            raise OverflowError("Stack Overflow")

        self._stack_pointer += 1

    def pop(self, target=None):
        if self._stack_pointer < 0:
            raise IndexError("Stack is empty")

        value = self._stack[self._stack_pointer]

        if target is None:
            pass
        elif hasattr(self, target.upper()):
            setattr(self, target.upper(), value)
        else:
            raise TypeError("Invalid target for pop()")

        self._stack_pointer -= 1

    def dump_stack(self):
        count = 0
        LOG.debug("Stack dump:")
        while count <= self._stack_pointer:
            LOG.debug("{:02X}h {:8X}".format(count, self._stack[count]))
            count += 1

    def inc(self, target):
        if hasattr(self, target.upper()):
            LOG.debug("Incrementing register {}".format(target.upper()))
            value = getattr(self, target.upper())
            try:
                setattr(self, target.upper(), value + 1)
            except exceptions.CarryOverException:
                self._EFLAGS |= 0x01
        else:
            raise ValueError("Invalid INC parameter")

    def dec(self, target):
        if hasattr(self, target.upper()):
            LOG.debug("Decrementing register {}".format(target.upper()))
            value = getattr(self, target.upper())
            try:
                setattr(self, target.upper(), value - 1)
            except exceptions.CarryOverException:
                self._EFLAGS |= 0x01
        else:
            raise ValueError("Invalid DEC parameter")

    # TODO: needs size check to only allow same size target and source
    def mov(self, target, src):
        if isinstance(src, Word):
            # src is memory address
            value = 0
        elif isinstance(src, str):
            # src is a register
            value = getattr(self, src.upper())
        elif isinstance(src, int):
            # src is plain integer
            value = src

        if isinstance(target, str):
            try:
                setattr(self, target.upper(), value)
            except exceptions.CarryOverException:
                self._EFLAGS |= 0x01

    """ Memory operations start here
    """

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


    """ Register operations start here
    """

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


    @property
    def EFLAGS(self):
        return self._EFLAGS

    @EFLAGS.setter
    def EFLAGS(self, value):
        raise TypeError("EFLAGS is a readonly register")
