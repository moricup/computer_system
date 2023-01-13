import sys
sys.path.append('../../')
from chap07.stage2 import codewriter_nand2tetris

class CodeWriter(codewriter_nand2tetris.CodeWriter):
    def __init__(self, asm):
        super().__init__(asm)
    
    def writeLabel(self, label):
        self.asm.write('(' + label + ')\n')

    def writeGoto(self, label):
        self.asm.write('@' + label +'\n')
        self.asm.write('0;JMP\n')

    def writeIf(self, label):
        self.subwrite_SPdownA()
        self.asm.write('D=M\n')
        self.asm.write('@' + label + '\n')
        self.asm.write('D;JNE\n')

class OurException(Exception):
    pass