from datatypes.byte import Byte
from datatypes.exceptions import CarryOverException

class Word(object):

    def __init__(self, value=0x0000):
        self._high = Byte(value & 0xff00)
        self._low = Byte(value & 0x00ff)

    @property
    def value(self):
        high = (self._high.value << 8) | 0xff
        low = self._low.value | 0xff00
        return (high & low)

    @value.setter
    def value(self, value):
        self._high.value =((value & 0xff00) >> 8)
        self._low.value = value & 0x00ff
        if value > 0xffff or value < 0x00:
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
        return [self._high.value, self._low.value]
