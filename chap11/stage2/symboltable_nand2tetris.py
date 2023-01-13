import sys
sys.path.append('../../')
from chap11.stage1 import symboltable_nand2tetris

class SymbolTable(symboltable_nand2tetris.SymbolTable):
    def __init__(self, jack_name, list_row_xml):
        super().__init__(jack_name, list_row_xml)

class OurException(Exception):
    pass