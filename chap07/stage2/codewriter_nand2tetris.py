import sys
sys.path.append('../../')
from chap07.stage1 import codewriter_nand2tetris

class CodeWriter(codewriter_nand2tetris.CodeWriter):
    def __init__(self, asm):
        super().__init__(asm)
        self.LIST_SEGMENTS_WITHOUT_LOOP = ['constant', 'static']
        self.LIST_SEGMENTS_WITH_LOOP = ['local', 'argument', 'this', 'that', 'pointer', 'temp']
    
    def writePushPop(self, commandtype, segment, index, file): # file is used only if segment=='static'
        if commandtype == 'C_PUSH':
            self.subwrite_address(segment, index, file)
            if segment == 'constant': # We use imaginary RAM which satisfies A==M.
                self.asm.write('D=A\n')
            else: # We use real RAM. 
                self.asm.write('D=M\n')
            self.asm.write('@SP\n')
            self.asm.write('A=M\n')
            self.asm.write('M=D\n')
            self.subwrite_SPup()
        elif commandtype == 'C_POP':
            self.subwrite_SPdownA()
            self.asm.write('D=M\n')
            self.subwrite_address(segment, index, file)
            self.asm.write('M=D\n')
        else:
            raise OurException('commandtype ' + commandtype + ' in writePushPop() is invalid.')
    
    def subwrite_address(self, segment, index, file):
        if segment in self.LIST_SEGMENTS_WITHOUT_LOOP:
            self.subwrite_address_without_loop(segment, index, file)
        elif segment in self.LIST_SEGMENTS_WITH_LOOP:
            self.subwrite_address_with_loop(segment, index)
        else:
            raise OurException('segment ' + segment + ' in subwrite_address() is invalid.')
    
    def subwrite_address_without_loop(self, segment, index, file):
        if segment == 'constant':
            address = index
        elif segment == 'static':
            address = file + '.' + index
        else:
            raise OurException('segment ' + segment + ' in subwrite_address_without_loop() is invalid.')
        self.asm.write('@' + address + '\n')
    
    def subwrite_address_with_loop(self, segment, index):
        if segment == 'local':
            self.asm.write('@LCL\n')
            self.asm.write('A=M\n')
        elif segment == 'argument':
            self.asm.write('@ARG\n')
            self.asm.write('A=M\n')
        elif segment == 'this':
            self.asm.write('@THIS\n')
            self.asm.write('A=M\n')
        elif segment == 'that':
            self.asm.write('@THAT\n')
            self.asm.write('A=M\n')
        elif segment == 'pointer':
            self.asm.write('@3\n')
        elif segment == 'temp':
            self.asm.write('@5\n')
        else:
            raise OurException('segment ' + segment + ' in subwrite_address_with_loop() is invalid.')
        for _ in range(int(index)):
            self.asm.write('A=A+1\n')

class OurException(Exception):
    pass