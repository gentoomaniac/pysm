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
    def __init__(self, screen, core):
        super().__init__()
        self._core = core
        self._screen = screen

    def run(self):
        LOG.info("Emulator started")
        core = Core()
        kernel = Kernel(core=core)

        msg = [ord(c) for c in "HELLO WORLD!"]
        msg.append(0x00)
        LOG.debug(len(msg))
        addr = stdlib.malloc(len(msg))
        length = len(msg)

        core.EAX = 4        # sys_write
        core.EBX = 1        # stderr
        core.ECX = addr
        core.EDX = length
        core.set_memory_range(addr, msg)

        kernel.interrupt(0x80)      # handover to kernel

        stdlib.free(addr)


def main():
    app = QApplication(sys.argv)
    screen = ScreenEGA(scale=4)
    screen.show()
    t = Emulator(screen, Kernel(screen=screen))
    t.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
