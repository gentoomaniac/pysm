import logging

from core import PySM_Core

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('interpreter')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)

class Interpreter(object):

    def __init__(self, instructions):
        self._instructions = instructions

        self._core = PySM_Core()

    def run(self):
        LOG.debug("Interpreting {} instructions".format(len(self._instructions)))
        for i in self._instructions:
            LOG.debug("{} {}, {}".format(i.instruction, i.parameters[0], i.parameters[1]))
            if i.instruction == 'MOV':
                setattr(self._core, i.parameters[0], int(i.parameters[1]))
                LOG.debug(self._core.dump_registers())
            elif i.instruction == 'INC':
                setattr(self._core, i.parameters[0], getattr(self._core, ))
                LOG.debug(self._core.dump_registers())

        memdump = self._core.dump_memory()
        LOG.debug("Memory dump:".format())
        for row in memdump:
            LOG.debug(row)

