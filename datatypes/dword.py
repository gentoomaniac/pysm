from datatypes.word import Word
from datatypes.exceptions import CarryOverException

class Dword(object):
    def __init__(self, value=0x00000000):
        self._high = Word(value & 0xffff0000)
        self._low = Word(value & 0x0000ffff)

    @property
    def value(self):
        high = (self._high.value << 16) | 0x0000ffff
        low = self._low.value | 0xffff0000
        return (high & low)

    @value.setter
    def value(self, value):
        self._high.value = ((value & 0xffff0000) >> 16)
        self._low.value = value & 0x0000ffff
        if value > 0xffffffff or value < 0x00:
            raise CarryOverException()

    @property
    def high(self):
        return self._high

    @high.setter
    def high(self, value):
        self._high.value = value

    @property
    def low(self):
        return self._low

    @low.setter
    def low(self, value):
        self._low.value = value

    def get_bytes(self):
        return self._high.get_bytes() + self._low.get_bytes()
