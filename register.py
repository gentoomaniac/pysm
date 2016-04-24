from datatypes.dword import Dword


class Register32(object):
    """ Base class for all registers
    """

    def __init__(self):
        self.__dword = Dword()

    @property
    def full(self):
        """ returns full register
        """
        return self.__dword.value

    @full.setter
    def full(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self.__dword.value = value

    @property
    def half(self):
        """ returns lowest 16 bit
        """
        return self.__dword.low.value

    @half.setter
    def half(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self.__dword.low.value = value

    @property
    def high(self):
        """ returns highest 8 bit of the lower 16 bit
        """
        return self.__dword.low.high.value

    @high.setter
    def high(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")

        self.__dword.low.high.value = value

    @property
    def low(self):
        """ returns lowest 8 bit of the register
        """
        return self.__dword.low.low.value

    @low.setter
    def low(self, value):
        if not isinstance(value, int):
            raise ValueError("Registers can only take integers")
        self.__dword.low.low.value = value
