import sys
sys.path.append('../../')
from chap10.stage2_2 import compilationengine_nand2tetris

class CompilationEngine(compilationengine_nand2tetris.CompilationEngine):
    def __init__(self, jack_name, list_row_xml_after_JackTokenizer):
        super().__init__(jack_name, list_row_xml_after_JackTokenizer)

class OurException(Exception):
    pass