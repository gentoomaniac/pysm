import json
import logging


import stdlib

from core import Core

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('interpreter')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)

class Interpreter(object):

    def __init__(self, instructions):
        self._instructions = instructions

        self._core = Core()

        self._pointer = {}

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


    # need to move to the interpreter
    def add_pointer(self, name, value=0x00):
        if name in self._pointer:
            raise ValueError("{} already exists".format(name))
        LOG.debug("Adding new pointer '{}' with value {:04X}".format(name, value))
        self._pointer[name] = value & 0xffff
        LOG.debug("Pointer table: {}".format(json.dumps(self._pointer, sort_keys=True)))


    def delete_pointer(self, name):
        if name in self._pointer:
            LOG.debug("Removed pointer '{}' with value {:04X}".format(name, self._pointer[name]))
            self._pointer.pop(name)
        LOG.debug("Pointer table: {}".format(json.dumps(self._pointer, sort_keys=True)))


    def get_pointer_value(self, name):
        return self._pointer.get(name, None)


    def set_pointer_value(self, name, value):
        if name not in self._pointer:
            raise ValueError("{} does not exist".format(name))
        self._pointer[name] = value & 0xffff
