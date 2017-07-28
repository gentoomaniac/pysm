import logging
import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

import stdlib
from core import Core
from kernel import Kernel
from screen import ScreenEGA

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('t_memory')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)


class Emulator(QThread):
    def __init__(self, core, screen):
        super().__init__()
        self.__core = core
        self.__screen = screen

    def run(self):
        LOG.info("Emulator started")
        kernel = Kernel(core=self.__core, screen=self.__screen)

        msg = [ord(c) for c in "HELLO WORLD!"]
        msg.append(0x00)
        LOG.debug(len(msg))
        addr = stdlib.malloc(len(msg))
        length = len(msg)

        self.__core.EAX = 4        # sys_write
        self.__core.EBX = 1        # stderr
        self.__core.ECX = addr
        self.__core.EDX = length
        self.__core.set_memory_range(addr, msg)

        kernel.interrupt(0x80)      # handover to kernel

        stdlib.free(addr)


def main():
    app = QApplication(sys.argv)
    screen = ScreenEGA(scale=2)
    screen.show()
    t = Emulator(core=Core(), screen=screen)
    t.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
