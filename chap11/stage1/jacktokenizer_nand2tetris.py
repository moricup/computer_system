import sys
sys.path.append('../../')
from chap10.stage1 import jacktokenizer_nand2tetris

class JackTokenizer(jacktokenizer_nand2tetris.JackTokenizer):
    def __init__(self, jack):
        super().__init__(jack)

class OurException(Exception):
    pass