class PySM_Core(object):

    def __init__(self):
        self._EAX = 0
        self._EBX = 0
        self._ECX = 0
        self._EDX = 0

        self._EIP = 0
        self._ESP = 0
        self._EBP = 0

        self._ESI = 0
        self._EDI = 0

        self._InstructionPointer = 0
        self._Flags = 0

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

    @property
    def AX(self):
        return self._EAX & 0xffff

    @AX.setter
    def AX(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        eax_masked = self._EAX | 0x0000ffff
        self._EAX = eax_masked & ((value & 0xffff) | 0xffff0000)

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
        #print("EAX:        {0:32b}".format(self._EAX))
        #print("eax_masked: {0:32b}".format(eax_masked))
        #print("value:      {0:32b}".format(value))
        #print("value lim:  {0:32b}".format(limited_value))
        #print("value shift:{0:32b}".format(shifted_value))
        #print("value mask: {0:32b}".format(masked_value))
        #print("AND:        {0:32b}".format(masked_value & eax_masked))
        self._EAX = masked_value & eax_masked       # merge the two masks into one new updated register
        #print("EAX after update: {}".format(self._EAX))

    @property
    def AL(self):
        return self._EAX & 0xff

    @AL.setter
    def AL(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        eax_masked = self._EAX | 0x000000ff
        self._EAX = eax_masked & ((value & 0xff) | 0xffffff00)


    @property
    def EBX(self):
        """ base register (32Bit)
        used in indexed addressing
        """
        return self._EBX & 0xffffffff


    @property
    def ECX(self):
        """ count register (32Bit)
        stores the loop count in iterative operations
        """
        return self._ECX & 0xffffffff


    @property
    def EDX(self):
        """ data register (32Bit)
        It is also used in input/output operations.
        It is also used with AX register along with DX for multiply and divide operations involving large values.
        """
        return self._EDX & 0xffffffff