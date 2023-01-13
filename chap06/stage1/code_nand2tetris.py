class Code:
    def __init__(self, line_asm):
        # variables for return
        self.comp = ''
        self.dest = ''
        self.jump = ''

        # We define self.dest_asm, self.comp_asm, and self.jump from line_asm.
        # see reference for detail
        line_asm_split_by_equal = line_asm.split('=')
        if len(line_asm_split_by_equal)==1:
            self.dest_asm = ''
            line_asm_without_dest = line_asm_split_by_equal[0]
        else:
            self.dest_asm = line_asm_split_by_equal[0]
            line_asm_without_dest = line_asm_split_by_equal[1]
        line_asm_without_dest_split_by_semicolon = line_asm_without_dest.split(';')
        if len(line_asm_without_dest_split_by_semicolon)==1:
            self.comp_asm = line_asm_without_dest_split_by_semicolon[0]
            self.jump_asm = ''
        else:
            self.comp_asm = line_asm_without_dest_split_by_semicolon[0]
            self.jump_asm = line_asm_without_dest_split_by_semicolon[1]
    
    def execute_comp(self): # see reference
        if self.comp_asm == '0':
            self.comp = '0101010'
        elif self.comp_asm == '1':
            self.comp = '0111111'
        elif self.comp_asm == '-1':
            self.comp = '0111010'
        elif self.comp_asm == 'D':
            self.comp = '0001100'
        elif self.comp_asm == 'A':
            self.comp = '0110000'
        elif self.comp_asm == '!D':
            self.comp = '0001101'
        elif self.comp_asm == '!A':
            self.comp = '0110001'
        elif self.comp_asm == '-D':
            self.comp = '0001111'
        elif self.comp_asm == '-A':
            self.comp = '0110011'
        elif self.comp_asm == 'D+1':
            self.comp = '0011111'
        elif self.comp_asm == 'A+1':
            self.comp = '0110111'
        elif self.comp_asm == 'D-1':
            self.comp = '0001110'
        elif self.comp_asm == 'A-1':
            self.comp = '0110010'
        elif self.comp_asm == 'D+A':
            self.comp = '0000010'
        elif self.comp_asm == 'D-A':
            self.comp = '0010011'
        elif self.comp_asm == 'A-D':
            self.comp = '0000111'
        elif self.comp_asm == 'D&A':
            self.comp = '0000000'
        elif self.comp_asm == 'D|A':
            self.comp = '0010101'
        elif self.comp_asm == 'M':
            self.comp = '1110000'
        elif self.comp_asm == '!M':
            self.comp = '1110001'
        elif self.comp_asm == '-M':
            self.comp = '1110011'
        elif self.comp_asm == 'M+1':
            self.comp = '1110111'
        elif self.comp_asm == 'M-1':
            self.comp = '1110010'
        elif self.comp_asm == 'D+M':
            self.comp = '1000010'
        elif self.comp_asm == 'D-M':
            self.comp = '1010011'
        elif self.comp_asm == 'M-D':
            self.comp = '1000111'
        elif self.comp_asm == 'D&M':
            self.comp = '1000000'
        elif self.comp_asm == 'D|M':
            self.comp = '1010101'
        else:
            assert(False)

    def execute_dest(self): # see reference
        if self.dest_asm == '':
            self.dest = '000'
        elif self.dest_asm == 'M':
            self.dest = '001'
        elif self.dest_asm == 'D':
            self.dest = '010'
        elif self.dest_asm == 'MD':
            self.dest = '011'
        elif self.dest_asm == 'A':
            self.dest = '100'
        elif self.dest_asm == 'AM':
            self.dest = '101'
        elif self.dest_asm == 'AD':
            self.dest = '110'
        elif self.dest_asm == 'AMD':
            self.dest = '111'
        else:
            assert(False)

    def execute_jump(self): # see reference
        if self.jump_asm == '':
            self.jump = '000'
        elif self.jump_asm == 'JGT':
            self.jump = '001'
        elif self.jump_asm == 'JEQ':
            self.jump = '010'
        elif self.jump_asm == 'JGE':
            self.jump = '011'
        elif self.jump_asm == 'JLT':
            self.jump = '100'
        elif self.jump_asm == 'JNE':
            self.jump = '101'
        elif self.jump_asm == 'JLE':
            self.jump = '110'
        elif self.jump_asm == 'JMP':
            self.jump = '111'
        else:
            assert(False)