import sys
sys.path.append('../../')
from chap07.stage1 import parser_nand2tetris

class Parser(parser_nand2tetris.Parser):
    def __init__(self, vm):
        super().__init__(vm)

class OurException(Exception):
    pass