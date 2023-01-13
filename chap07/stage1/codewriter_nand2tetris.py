class CodeWriter:
    def __init__(self, asm):
        # asm file for writing
        self.asm = asm
        # classification of operators
        self.LIST_UNARY_OPERATORS = ['neg', 'not']
        self.LIST_BINARY_ARITHMETICAL_OPERATORS = ['add', 'sub', 'and', 'or']
        self.LIST_BINARY_COMPARISONAL_OPERATORS = ['eq', 'gt', 'lt']
        # label index for branching
        self.label_idx = 0
    
    def writeArithmetic(self, command):
        # see reference
        if command in self.LIST_UNARY_OPERATORS:
            self.subwrite_unary_operators(command)
        elif command in self.LIST_BINARY_ARITHMETICAL_OPERATORS:
            self.subwrite_binary_arithmetical_operators(command)
        elif command in self.LIST_BINARY_COMPARISONAL_OPERATORS:
            self.subwrite_binary_comparisonal_operators(command)
        else:
            raise OurException('command ' + command + ' in writeArithmetic() is invalid.')
    
    def subwrite_unary_operators(self, command):
        self.subwrite_SPdownA()
        if command == 'neg':
            self.asm.write('M=-M\n')
        elif command == 'not':
            self.asm.write('M=!M\n')
        else:
            raise OurException('command ' + command + ' in subwrite_unary_operator() is invalid.')
        self.subwrite_SPup()
    
    def subwrite_binary_arithmetical_operators(self, command):
        self.subwrite_SPdownA()
        self.asm.write('D=M\n')
        self.subwrite_SPdownA()
        if command == 'add':
            self.asm.write('M=D+M\n')
        elif command == 'sub':
            self.asm.write('M=M-D\n')
        elif command == 'and':
            self.asm.write('M=D&M\n')
        elif command == 'or':    
            self.asm.write('M=D|M\n')
        else:
            raise OurException('command ' + command + ' in subwrite_binary_arithmetical_operators() is invalid.')
        self.subwrite_SPup()
    
    def subwrite_binary_comparisonal_operators(self, command):
        # Prepare two labels
        label_true_start = 'LABEL' + str(self.label_idx)
        self.label_idx += 1
        label_false_end = 'LABEL' + str(self.label_idx)
        self.label_idx += 1

        self.subwrite_SPdownA()
        self.asm.write('D=M\n')
        self.subwrite_SPdownA()
        self.asm.write('D=M-D\n')
        self.asm.write('@' + label_true_start + '\n')
        if command == 'eq':
            self.asm.write('D;JEQ\n')
        elif command == 'gt':
            self.asm.write('D;JGT\n')
        elif command == 'lt':
            self.asm.write('D;JLT\n')
        else:
            raise OurException('command ' + command + ' in subwrite_binary_comparisonal_operators() is invalid.')
        self.asm.write('@SP\n')
        self.asm.write('A=M\n')
        self.asm.write('M=0\n')
        self.asm.write('@' + label_false_end + '\n')
        self.asm.write('0;JMP\n')
        self.asm.write('(' + label_true_start + ')\n')
        self.asm.write('@SP\n')
        self.asm.write('A=M\n')
        self.asm.write('M=-1\n')
        self.asm.write('(' + label_false_end + ')\n')
        self.subwrite_SPup()

    def subwrite_SPdownA(self):
        self.asm.write('@SP\n')
        self.asm.write('M=M-1\n')
        self.asm.write('A=M\n')

    def subwrite_SPup(self):
        self.asm.write('@SP\n')
        self.asm.write('M=M+1\n')
    
    def writePushPop(self, commandtype, segment, index):
        if commandtype == 'C_PUSH':
            if segment == 'constant':
                self.asm.write('@' + index + '\n')
                self.asm.write('D=A\n')
                self.asm.write('@SP\n')
                self.asm.write('A=M\n')
                self.asm.write('M=D\n')
                self.subwrite_SPup()
            else:
                raise OurException('segment ' + segment + ' in writePushPop() is invalid.')
        else:
            raise OurException('commandtype ' + commandtype + ' in writePushPop() is invalid.')


class OurException(Exception):
    pass