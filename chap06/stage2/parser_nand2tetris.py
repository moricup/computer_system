import code_nand2tetris
import symboltable_nand2tetris
import sys
sys.path.append('../../')
from chap06.stage1 import parser_nand2tetris

class Parser(parser_nand2tetris.Parser):
    def __init__(self, asm):
        super().__init__(asm)
        self.symboltable = symboltable_nand2tetris.SymbolTable()
        self.reservedRAM = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15']
    
    def execute_asm_1st(self):
        row_counta = 0
        for line_asm in self.asm:
            # delete unnecessary chars
            line_asm = self.delete_blank_newline_comment(line_asm)
            if line_asm == '': # Ignore null-string
                continue
            if line_asm[0] == '(': # if symbols (Xxx), add symbol directly to memorize row_counta
                line_asm = line_asm.replace('(', '')
                line_asm = line_asm.replace(')', '')
                self.symboltable.table[line_asm] = format(row_counta, 'b').zfill(15)
            else: # if the others, add counta
                row_counta += 1

    def execute_asm_2nd(self):
        self.execute_asm()

    def symbol(self, line_asm):
        # delete the symbol '@'
        line_asm = line_asm.replace('@', '')
        if line_asm.isnumeric(): # if numeric, this is an address
            return format(int(line_asm), 'b').zfill(15)
        elif line_asm == 'SP': # reserved symbol
            return format(0, 'b').zfill(15)
        elif line_asm == 'LCL': # reserved symbol
            return format(1, 'b').zfill(15)
        elif line_asm == 'ARG': # reserved symbol
            return format(2, 'b').zfill(15)
        elif line_asm == 'THIS': # reserved symbol
            return format(3, 'b').zfill(15)
        elif line_asm == 'THAT': # reserved symbol
            return format(4, 'b').zfill(15)
        elif line_asm in self.reservedRAM: # reserved symbol
            return format(int(line_asm.replace('R', '')), 'b').zfill(15)
        elif line_asm == 'SCREEN': # reserved symbol
            return format(16384, 'b').zfill(15)
        elif line_asm == 'KBD': #reserved symbol
            return format(24576, 'b').zfill(15)
        else: # We have a symbol defined by us.
            if self.symboltable.contains(line_asm) == False:
                self.symboltable.addEntry(line_asm)
            return self.symboltable.getAddress(line_asm)
    
    def delete_blank_newline_comment(self, str):
        # delete blank
        str = str.replace(' ', '')
        # delete a new line
        str = str.replace('\n', '')
        # delete a comment at the end
        str = str.split('/')[0]
        # return
        return str