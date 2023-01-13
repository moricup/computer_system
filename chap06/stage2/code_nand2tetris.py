import sys
sys.path.append('../../')
from chap06.stage1 import code_nand2tetris

class Code(code_nand2tetris.Code):
    def __init__(self, line_asm):
        super().__init__(line_asm)