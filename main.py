import logging
import nltk
import sys

from instruction import Instruction
from interpreter import Interpreter

FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message)s'
LOG = logging.getLogger('main')
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(FORMAT))
LOG.addHandler(ch)


def main():
    instructions = []
    tokens = tokenize("input.asm")
    for t in tokens:
        ins = Instruction()
        ins.instruction = t[0].upper()
        try:
            ins.parameters.append(t[1].upper())
            ins.parameters.append(t[3].upper())
        except:
            pass

        instructions.append(ins)

    interpreter = Interpreter(instructions)
    interpreter.run()


def prepare_nltk():
    """ Download nltk tokenizer data files"""
    nltk.download(info_or_id='punkt')


def tokenize(file):
    prepare_nltk()
    try:
        with open(file , "r") as f:
            lines = f.readlines()
            return [nltk.word_tokenize(l) for l in lines]

    except Exception as e:
        LOG.error("Couldn't read input file: {}".format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()