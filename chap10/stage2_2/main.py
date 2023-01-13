import json
import jacktokenizer_nand2tetris
import compilationengine_nand2tetris
import os

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

def main():
    # get settings
    with open('settings.json', 'r') as json_file:
        json_data = json.load(json_file)
    path_chap10 = json_data['path_chap10']
    list_dir = json_data['list_dir']
    
    # Execute translating from multiple *.jack to *_ans.xml
    for dir in list_dir:
        # Get list of file_name for test_name
        list_file_name = os.listdir(path_chap10 + dir)

        # Get list of jack_name from list_file_name
        list_jack_name = get_list_jack_name(list_file_name)
        
        # Execute translating from each (jack_name+'.jack') to (jack_name+'_ans.xml')
        for jack_name in list_jack_name:
            # Prepare jack and generate JackTokenizer
            with open(path_chap10 + dir + '/' + jack_name + '.jack', 'r') as jack:
                jacktokenizer = jacktokenizer_nand2tetris.JackTokenizer(jack)

            # Get list_row_xml_after_JackTokenizer from jacktokenizer
            list_row_xml_after_JackTokenizer = get_list_row_xml_after_JackTokenizer(jacktokenizer)

            # Write *T_ans.xml
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

class OurException(Exception):
    pass

if __name__ == '__main__':
    main()