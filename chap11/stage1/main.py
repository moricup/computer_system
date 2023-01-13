import json
import jacktokenizer_nand2tetris
import compilationengine_nand2tetris
import symboltable_nand2tetris
import os
import csv

def get_list_jack_name(list_file_name):
    list_jack_name = []
    for file_name in list_file_name:
        if len(file_name.split('.'))==1: # Dismiss dir
            continue
        file_name_without_extension, file_extension = file_name.split('.')
        if file_extension == 'jack': # extension is jack
            list_jack_name.append(file_name_without_extension)
    return list_jack_name

def get_list_row_xml_after_JackTokenizer(jacktokenizer):
    list_row_xml_after_JackTokenizer = []
    while(jacktokenizer.hasMoreTokens()):
        # Get tokenType_from_jacktokenizer
        tokenType_from_jacktokenizer = jacktokenizer.tokenType()

        # Get tokenType and token
        if tokenType_from_jacktokenizer == 'KEYWORD':
            tokenType = 'keyword'
            token = jacktokenizer.keyWord().lower()
        elif tokenType_from_jacktokenizer == 'SYMBOL':
            tokenType = 'symbol'
            token = jacktokenizer.symbol()
        elif tokenType_from_jacktokenizer == 'IDENTIFIER':
            tokenType = 'identifier'
            token = jacktokenizer.identifier()
        elif tokenType_from_jacktokenizer == 'INT_CONST':
            tokenType = 'integerConstant'
            token = jacktokenizer.intVal()
        elif tokenType_from_jacktokenizer == 'STRING_CONST':
            tokenType = 'stringConstant'
            token = jacktokenizer.stringVal()
        else:
            raise OurException('tokenType ' + tokenType + ' in main() is invalid.')
        
        # Replace escape
        token = escape_for_xml(token)

        # Write one-line
        list_row_xml_after_JackTokenizer.append('<' + tokenType + '> ' + token + ' </' + tokenType + '>')
    
    return list_row_xml_after_JackTokenizer

def escape_for_xml(token):
    token = token.replace('&', '&amp;')
    token = token.replace('<', '&lt;')
    token = token.replace('>', '&gt;')
    return token

def write_file_from_list_row_file(file, list_row_file):
    for row_file in list_row_file:
        file.write(row_file + '\n')

def make_csv_of_SymbolTable(path_chap10, dir, jack_name, dict_class_symbolTable, dict_dict_method_symbolTable):
    # Make dir of SymbolTable
    path_to_SymbolTable = path_chap10 + dir + '/' + jack_name + '_SymbolTable'
    os.makedirs(path_to_SymbolTable, exist_ok = True)
    # Make csv of dict_class_symbolTable
    with open(path_to_SymbolTable + '/class_' + jack_name + '.csv', 'w', newline='') as csv_file:
        make_one_csv(csv_file, dict_class_symbolTable)
    # Make each csv in dict_dict_method_symbolTable
    for method_name in dict_dict_method_symbolTable.keys():
        dict_method_symbolTable = dict_dict_method_symbolTable[method_name]
        with open(path_to_SymbolTable + '/method_' + method_name + '.csv', 'w', newline='') as csv_file:
            make_one_csv(csv_file, dict_method_symbolTable)

def make_one_csv(csv_file, dict_symbolTable):
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['identifier', 'type', 'kind', 'index'])
    for identifier in dict_symbolTable.keys():
        csv_writer.writerow([identifier,] + dict_symbolTable[identifier])

def main():
    # get settings
    with open('settings.json', 'r') as json_file:
        json_data = json.load(json_file)
    path_chap10 = json_data['path_chap10'] # Use the path to chap10, although we are in chap11
    list_dir = json_data['list_dir']
    
    # Execute translating from multiple *.jack to *_ans.xml
    # and generate multiple SymbolTable
    for dir in list_dir:
        # Get list of file_name for test_name
        list_file_name = os.listdir(path_chap10 + dir)

        # Get list of jack_name from list_file_name
        list_jack_name = get_list_jack_name(list_file_name)
        
        # Execute translating from each (jack_name+'.jack') to (jack_name+'_ans.xml')
        # and generate dir (jack_name+'SymbolTable')
        for jack_name in list_jack_name:
            # Prepare jack and generate JackTokenizer
            with open(path_chap10 + dir + '/' + jack_name + '.jack', 'r') as jack:
                jacktokenizer = jacktokenizer_nand2tetris.JackTokenizer(jack)

            # Get list_row_xml_after_JackTokenizer from jacktokenizer
            list_row_xml_after_JackTokenizer = get_list_row_xml_after_JackTokenizer(jacktokenizer)

            # Write *T_ans.xml if we need it.
            with open(path_chap10 + dir + '/' + jack_name + 'T_ans.xml', 'w') as xml_after_JackTokenizer:
                xml_after_JackTokenizer.write('<tokens>\n')
                write_file_from_list_row_file(xml_after_JackTokenizer, list_row_xml_after_JackTokenizer)
                xml_after_JackTokenizer.write('</tokens>\n')

            # Generate CompilationEngine
            compilationengine = compilationengine_nand2tetris.CompilationEngine(jack_name, list_row_xml_after_JackTokenizer)

            # Get list_row_xml
            list_row_xml = compilationengine.output_list_row_xml()

            # Write *_ans.xml
            with open(path_chap10 + dir + '/' + jack_name + '_ans.xml', 'w') as xml:
                write_file_from_list_row_file(xml, list_row_xml)
            
            # Generate SymbolTable
            symboltable = symboltable_nand2tetris.SymbolTable(jack_name, list_row_xml)

            # Get dict
            dict_class_symbolTable, dict_dict_method_symbolTable = symboltable.output()

            # Make csv of SymbolTable
            make_csv_of_SymbolTable(path_chap10, dir, jack_name, dict_class_symbolTable, dict_dict_method_symbolTable)

class OurException(Exception):
    pass

if __name__ == '__main__':
    main()