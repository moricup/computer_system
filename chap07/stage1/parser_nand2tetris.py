class Parser:
    def __init__(self, vm):
        # list of row_vm without new line
        self.vm = [row_vm.replace('\n', '') for row_vm in vm.readlines()]
        # row_idx in vm which we are reading
        self.row_idx = 0
        # row_vm which we are reading
        self.row_vm = ''
        # list of arithmetic commands
        self.arithmetic_commands = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
    
    def hasMoreCommands(self):
        while(True):
            if self.row_idx == len(self.vm): # if we are in end in vm, return False
                return False
            # Read row in vm
            row_vm = self.vm[self.row_idx]
            if row_vm == '': # if row_vm is none (origin is new line), read next line
                self.row_idx += 1
                continue
            if row_vm[0] == '/': # if row_vm is comment, read next line
                self.row_idx += 1
                continue
            # Now, row_vm is some command. Return True.
            return True

    def advance(self):
        # save self.row_vm without comment at end
        self.row_vm = self.vm[self.row_idx].split('/')[0]
        # increment row_idx for next hasMoreCommands
        self.row_idx += 1
        # read command
        command = self.row_vm.split(' ')[0]
        # return
        return command
    
    def commandType(self, command):
        # see reference
        if command == 'push':
            return 'C_PUSH'
        elif command == 'pop':
            return 'C_POP'
        elif command == 'label':
            return 'C_LABEL'
        elif command == 'goto':
            return 'C_GOTO'
        elif command == 'if-goto':
            return 'C_IF'
        elif command == 'function':
            return 'C_FUNCTION'
        elif command == 'call':
            return 'C_CALL'
        elif command == 'return':
            return 'C_RETURN'
        elif command in self.arithmetic_commands:
            return 'C_ARITHMETIC'
        else:
            raise OurException('command ' + command + ' in commandType() is invalid.')
        
    def arg1(self, commandtype):
        # see reference
        if commandtype == 'C_ARITHMETIC':
            return self.row_vm # This is command
        else:
            return self.row_vm.split(' ')[1]
    
    def arg2(self):
        # see reference
        return self.row_vm.split(' ')[2]

class OurException(Exception):
    pass