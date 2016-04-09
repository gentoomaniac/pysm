from datatypes.exceptions import CarryOverException

class Byte(object):
    def __init__(self, value=0x00):
        self._data = value & 0xff

    @property
    def value(self):
        return self._data

    @value.setter
    def value(self, value):
        """ set the bytes value

        :param value: thew value of the byte
        :return: True if an overflow happened, else False
        """
        self._data = value & 0xff
        if value > 0xff:
            raise CarryOverException()
