class Register(object):
    """ Base class for all registers
    """

    def __init__(self):
        self.__value = 0

    @property
    def full(self):
        """ primary accumulator (32Bit)
        it is used in input/output and most arithmetic instructions. For example, in multiplication operation,
        one operand is stored in EAX or AX or AL register according to the size of the operand
        """
        return  self.__value & 0xffffffff

    @full.setter
    def full(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self.__value = value & 0xffffffff

    @property
    def half(self):
        return  self.__value & 0xffff

    @half.setter
    def half(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self.__value = ( self.__value | 0x0000ffff) & ((value & 0xffff) | 0xffff0000)

    @property
    def high(self):
        return ( self.__value & 0xff00) >> 8

    @high.setter
    def high(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        limited_value = value & 0xff  # limit the value to 8 bits
        shifted_value = limited_value << 8  # shift those bits to the right position
        masked_value = shifted_value | 0xffff00ff  # mask the bits we don't want to update

        eax_masked =  self.__value | 0x0000ff00  # mask out the bits we want to update
        self.__value = masked_value & eax_masked  # merge the two masks into one new updated register

    @property
    def low(self):
        return  self.__value & 0xff

    @low.setter
    def low(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self.__value = ( self.__value | 0x000000ff) & ((value & 0xff) | 0xffffff00)
