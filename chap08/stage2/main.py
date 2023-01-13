import json
import parser_nand2tetris
import codewriter_nand2tetris
import os

def main():
    # get settings
    with open('settings.json', 'r') as json_file:
        json_data = json.load(json_file)
    path_chap8 = json_data['path_chap8']
    one_dir = json_data['one_dir']
    list_test_name = json_data['list_test_name']

    # list of commandtypes for using arg2 or not
    LIST_COMMANDTYPES_FOR_ARG2 = ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']
    
    # Execute translating from multiple vm to asm <- a new point from chap08.stage1
    for test_name in list_test_name:
        # Get list of file_name for test_name
        list_file_name = os.listdir(path_chap8 + one_dir + test_name)
        # Does there exist 'Sys.vm' ?
        if 'Sys.vm' in list_file_name:
            does_sys_vm_exist = True
        else:
            does_sys_vm_exist = False
        # Prepare one asm and generate codewriter
        asm = open(path_chap8 + one_dir + test_name + '/' + test_name + '.asm', 'w')
        codewriter = codewriter_nand2tetris.CodeWriter(asm, does_sys_vm_exist)
        # Get list of path of vm_file
        list_path_vm_file = []
        for file_name in list_file_name:
            if file_name.split('.')[1] == 'vm': # extension is vm
                list_path_vm_file.append(path_chap8 + one_dir + test_name + '/' + file_name)
        # Execute translating from each vm to asm
        for path_vm_file in list_path_vm_file:
            # Prepare each vm and generate parser
            vm = open(path_vm_file, 'r')
            parser = parser_nand2tetris.Parser(vm)
            while parser.hasMoreCommands(): # Keep translating as long as you have the command.
                command = parser.advance()
                commandtype = parser.commandType(command)
                if commandtype != 'C_RETURN':
                    arg1 = parser.arg1(commandtype)
                    if commandtype in LIST_COMMANDTYPES_FOR_ARG2:
                        arg2 = parser.arg2()
                        if commandtype == 'C_PUSH' or commandtype == 'C_POP':
                            vm_name = get_vm_name(path_vm_file)
                            codewriter.writePushPop(commandtype, arg1, arg2, vm_name)
                        elif commandtype == 'C_FUNCTION':
                            codewriter.writeFunction(arg1, arg2)
                        elif commandtype == 'C_CALL':
                            codewriter.writeCall(arg1, arg2)
                        else:
                            raise OurException('commandtype ' + commandtype + 'is invalid when arg2 is defined.')
                    elif commandtype == 'C_ARITHMETIC':
                        codewriter.writeArithmetic(command)
                    elif commandtype == 'C_LABEL':
                        codewriter.writeLabel(arg1)
                    elif commandtype == 'C_GOTO':
                        codewriter.writeGoto(arg1)
                    elif commandtype == 'C_IF':
                        codewriter.writeIf(arg1)
                    else:
                        raise OurException('commandtype' + commandtype + ' is invalid when arg2 is not defined.')
                else:
                    codewriter.writeReturn()
                            
            # end of translating for each vm
            vm.close()
        # end of translating for each asm
        asm.close()

def get_vm_name(path_vm_file):
    vm_name_with_extension = path_vm_file.split('/')[-1]
    vm_name = vm_name_with_extension.split('.')[0]
    return vm_name

class OurException(Exception):
    pass

if __name__ == '__main__':
    main()