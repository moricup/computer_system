import sys
sys.path.append('../../')
from chap08.stage1 import codewriter_nand2tetris

class CodeWriter(codewriter_nand2tetris.CodeWriter):
    def __init__(self, asm, does_sys_vm_exist):
        super().__init__(asm)
        self.return_idx = 0
        # If 'Sys.vm' exists, execute initialization
        if does_sys_vm_exist:
            self.writeInit()
    
    def writeInit(self):
        self.asm.write('@256\n')
        self.asm.write('D=A\n')
        self.asm.write('@SP\n')
        self.asm.write('M=D\n')
        self.writeCall('Sys.init', 0)

    def writeFunction(self, functionName, numLocals): # numLocals is string
        self.asm.write('(' + functionName + ')\n')
        # Initialize local numbers whose the number of pieces is numLocals.
        for _ in range(int(numLocals)):
            self.writePushPop('C_PUSH', 'constant', '0', '_')


    def writeCall(self, functionName, numArgs): # numArgs is string
        label_return_address = 'LABEL' + str(self.label_idx)
        self.label_idx += 1

        # Push the state of caller
        self.subwrite_push_M(label_return_address, True)
        self.subwrite_push_M('LCL', False)
        self.subwrite_push_M('ARG', False)
        self.subwrite_push_M('THIS', False)
        self.subwrite_push_M('THAT', False)

        # Shift ARG
        self.asm.write('@SP\n')
        self.asm.write('D=M\n')
        self.asm.write('@ARG\n')
        self.asm.write('M=D\n')
        for _ in range(int(numArgs)+5):
            self.asm.write('M=M-1\n')
        
        # Shift LCL
        self.asm.write('@SP\n')
        self.asm.write('D=M\n')
        self.asm.write('@LCL\n')
        self.asm.write('M=D\n')

        # goto function
        self.writeGoto(functionName)

        # Write the label of return address
        self.asm.write('(' + label_return_address + ')\n')

    def writeReturn(self):
        symbol_FRAME = 'FRAME' + str(self.return_idx)
        symbol_RET = 'RET' + str(self.return_idx)
        self.return_idx += 1

        # Save LCL to FRAME
        self.asm.write('@LCL\n')
        self.asm.write('D=M\n')
        self.asm.write('@' + symbol_FRAME + '\n')
        self.asm.write('M=D\n')

        # Save return_address to RET
        self.asm.write('A=M\n')
        for _ in range(5):
            self.asm.write('A=A-1\n')
        self.asm.write('D=M\n')
        self.asm.write('@' + symbol_RET + '\n')
        self.asm.write('M=D\n')

        # Save return_value to ARG
        self.subwrite_SPdownA()
        self.asm.write('D=M\n')
        self.asm.write('@ARG\n')
        self.asm.write('A=M\n')
        self.asm.write('M=D\n')

        # Restore SP to caller
        self.asm.write('@ARG\n')
        self.asm.write('D=M\n')
        self.asm.write('@SP\n')
        self.asm.write('M=D+1\n')

        # Restore addresses to caller
        self.subwrite_restore_address('THAT', symbol_FRAME, 1)
        self.subwrite_restore_address('THIS', symbol_FRAME, 2)
        self.subwrite_restore_address('ARG', symbol_FRAME, 3)
        self.subwrite_restore_address('LCL', symbol_FRAME, 4)

        # goto return_address
        self.asm.write('@' + symbol_RET + '\n')
        self.asm.write('A=M\n')
        self.asm.write('0;JMP\n')

    def subwrite_push_M(self, address, isLabel):
        self.asm.write('@' + address + '\n')
        if isLabel is True:
            self.asm.write('D=A\n')
        else:
            self.asm.write('D=M\n')
        self.asm.write('@SP\n')
        self.asm.write('A=M\n')
        self.asm.write('M=D\n')
        self.subwrite_SPup()
    
    def subwrite_restore_address(self, symbol, symbol_FRAME, lag_from_FRAME):
        self.asm.write('@' + symbol_FRAME + '\n')
        self.asm.write('A=M\n')
        for _ in range(lag_from_FRAME):
            self.asm.write('A=A-1\n')
        self.asm.write('D=M\n')
        self.asm.write('@' + symbol + '\n')
        self.asm.write('M=D\n')

class OurException(Exception):
    pass