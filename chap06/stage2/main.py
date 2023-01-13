import json
import parser_nand2tetris

def main():
    # get settings
    with open('settings.json', 'r') as json_file:
        json_data = json.load(json_file)
    path_chap6 = json_data['path_chap6']
    list_dir = json_data['list_dir']
    list_asm = json_data['list_asm']
    list_hack = json_data['list_hack']
    
    # Execute Assembling for each asm
    for idx in range(len(list_dir)):
        path_asm = path_chap6 + list_dir[idx] + list_asm[idx]
        with open(path_asm, 'r') as asm:
            parser = parser_nand2tetris.Parser(asm)
            # 1st loop
            parser.execute_asm_1st()
            # Move the iterator to the beginning.
            parser.asm.seek(0)
            # 2nd loop
            parser.execute_asm_2nd()
            # Write hack
            path_hack = path_chap6 + list_dir[idx] + list_hack[idx]
            with open(path_hack, 'w') as hack:
                hack.write(parser.hack)

if __name__ == '__main__':
    main()