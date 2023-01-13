import json
import parser_nand2tetris
import codewriter_nand2tetris

def main():
    # get settings
    with open('settings.json', 'r') as json_file:
        json_data = json.load(json_file)
    path_chap7 = json_data['path_chap7']
    list_dir = json_data['list_dir']
    dict_list_file = json_data['dict_list_file']

    # list of commandtypes for using arg2 or not
    LIST_COMMANDTYPES_FOR_ARG2 = ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']
    
    # Execute translating from vm to asm
    for dir in list_dir:
        list_file = dict_list_file[dir]
        for file in list_file:
            # Prepare files and generate instances
            path_file_without_extension = path_chap7 + dir + file + '/' + file
            vm = open(path_file_without_extension + '.vm', 'r')
            asm = open(path_file_without_extension + '.asm', 'w')
            parser = parser_nand2tetris.Parser(vm)
            codewriter = codewriter_nand2tetris.CodeWriter(asm)

            while parser.hasMoreCommands(): # Keep translating as long as you have the command.
                command = parser.advance()
                commandtype = parser.commandType(command)
                if commandtype != 'C_RETURN':
                    arg1 = parser.arg1(commandtype)
                    if commandtype in LIST_COMMANDTYPES_FOR_ARG2:
                        arg2 = parser.arg2()
                        if commandtype == 'C_PUSH' or commandtype == 'C_POP':
                            codewriter.writePushPop(commandtype, arg1, arg2, file)
                        else:
                            raise OurException('commandtype ' + commandtype + 'is invalid when arg2 is defined.')
                    elif commandtype == 'C_ARITHMETIC':
                        codewriter.writeArithmetic(command)
                    else:
                        raise OurException('commandtype' + commandtype + ' is invalid when arg2 is not defined.')
                else:
                    raise OurException('commandtype ' + commandtype + ' is invalid when arg1 and arg2 are not defined.')
                            
            # end of translating for one file
            vm.close()
            asm.close()

class OurException(Exception):
    pass

if __name__ == '__main__':
    main()