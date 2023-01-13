import sys
sys.path.append('../../')
from chap10.stage2_1 import compilationengine_nand2tetris

class CompilationEngine(compilationengine_nand2tetris.CompilationEngine):
    def __init__(self, jack_name, list_row_xml_after_JackTokenizer):
        # row_xml_after_JackTokenizer_next and token_next which we are reading NEXT from update_state()
        self.row_xml_after_JackTokenizer_next = ''
        self.token_next = ''
        self.tokenType_next = ''
        
        # list of unaryOp
        self.LIST_UNARYOP = ['-', '~']
        # list of KeywordConstant
        self.LIST_KEYWORDCONSTANT = ['true', 'false', 'null', 'this']

        super().__init__(jack_name, list_row_xml_after_JackTokenizer)
    
    def update_state(self):
        # update if we are not in end
        if self.list_row_xml_after_JackTokenizer_idx < len(self.list_row_xml_after_JackTokenizer):
            self.row_xml_after_JackTokenizer = self.list_row_xml_after_JackTokenizer[self.list_row_xml_after_JackTokenizer_idx]
            self.tokenType = self.row_xml_after_JackTokenizer.split(' ')[0].replace('<','').replace('>','')
            self.token = self.row_xml_after_JackTokenizer.replace('<'+self.tokenType+'> ','').replace(' </'+self.tokenType+'>','')
            self.list_row_xml_after_JackTokenizer_idx += 1
            # add next state if there exists
            if self.list_row_xml_after_JackTokenizer_idx < len(self.list_row_xml_after_JackTokenizer):
                self.row_xml_after_JackTokenizer_next = self.list_row_xml_after_JackTokenizer[self.list_row_xml_after_JackTokenizer_idx]
                self.tokenType_next = self.row_xml_after_JackTokenizer_next.split(' ')[0].replace('<','').replace('>','')
                self.token_next = self.row_xml_after_JackTokenizer_next.replace('<'+self.tokenType_next+'> ','').replace(' </'+self.tokenType_next+'>','')

    # --- expression ---

    def compileTerm(self):
        # Delimit begin of term
        self.delimit_begin('term')
        if self.tokenType == 'integerConstant': # Append integerConstant
            self.append_state()
        elif self.tokenType == 'stringConstant': # Append integerConstant
            self.append_state()
        elif self.token in self.LIST_KEYWORDCONSTANT: # Write KeywordConstant
            self.write_KeywordConstant()
        elif self.token == '(': # Append '(' if there exist
            self.append_state('(')
            # Generate tree of expression
            self.compileExpression()
            # Append ')'
            self.append_state(')')
        elif self.token in self.LIST_UNARYOP: # Write unaryOp
            self.write_unaryOp()
            # Generate tree of term
            self.compileTerm()
        elif self.token_next == '[': # Write array
            # Write varName
            self.write_varName()
            # Append '['
            self.append_state('[')
            # Generate tree of expression
            self.compileExpression()
            # Append ']'
            self.append_state(']')
        elif self.token_next == '(' or self.token_next == '.': # Write subroutineCall
            self.write_subroutineCall()
        else: # Write varName
            self.write_varName()
        # Delimit end of term
        self.delimit_end('term')

    def write_unaryOp(self):
        # Append unaryOp
        self.append_state(self.LIST_UNARYOP)
    
    def write_KeywordConstant(self):
        # Append KeywordConstant
        self.append_state(self.LIST_KEYWORDCONSTANT)

class OurException(Exception):
    pass