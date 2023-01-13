import code_nand2tetris

class Parser:
    def __init__(self, asm):
        self.asm = asm
        self.hack = ''
    
    def execute_asm(self):
        for line_asm in self.asm:
            # delete unnecessary chars
            line_asm = self.delete_blank_newline_comment(line_asm)
            # Ignore null-string
            if line_asm == '':
                continue
            # Ignore symbol (Xxx)
            if line_asm[0] == '(':
                continue

            # We write something in this roop. Then add a new line in hack if not beginning.
            if self.hack != '':
                self.hack += '\n'

            # Branch A-command or C-command
            if line_asm[0] == '@':
                self.hack += '0'
                self.hack += self.symbol(line_asm)
            else:
                code = code_nand2tetris.Code(line_asm)
                code.execute_comp()
                code.execute_dest()
                code.execute_jump()
                # 111 comp dest jump
                self.hack += '111'
                self.hack += code.comp
                self.hack += code.dest
                self.hack += code.jump

    def symbol(self, line_asm):
        return format(int(line_asm[1:]), 'b').zfill(15)
    
    def delete_blank_newline_comment(self, str):
        # delete blank
        str = str.replace(' ', '')
        # delete a new line
        str = str.replace('\n', '')
        # delete a comment at the end
        str = str.split('/')[0]
        # return
        return str