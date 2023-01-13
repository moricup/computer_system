class CompilationEngine:
    def __init__(self, jack_name, list_row_xml_after_JackTokenizer):
        # Save argments
        self.jack_name = jack_name
        self.list_row_xml_after_JackTokenizer = list_row_xml_after_JackTokenizer
        # index which we are reading now
        self.list_row_xml_after_JackTokenizer_idx = 0
        # row_xml_after_JackTokenizer and token which we are reading now from update_state()
        self.row_xml_after_JackTokenizer = ''
        self.token = ''
        self.tokenType = ''
        # list for output
        self.list_row_xml = []

        # list of op
        # '&amp;' is '&'
        # '&lt;' is '<'
        # '&gt;' is '>'
        self.LIST_OP = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']

        # Initialize state
        self.update_state()
        # Begin compiling
        self.compileClass()
    
    def output_list_row_xml(self):
        return self.list_row_xml
    
    def update_state(self):
        # update if we are not in end
        if self.list_row_xml_after_JackTokenizer_idx < len(self.list_row_xml_after_JackTokenizer):
            self.row_xml_after_JackTokenizer = self.list_row_xml_after_JackTokenizer[self.list_row_xml_after_JackTokenizer_idx]
            self.tokenType = self.row_xml_after_JackTokenizer.split(' ')[0].replace('<','').replace('>','')
            self.token = self.row_xml_after_JackTokenizer.replace('<'+self.tokenType+'> ','').replace(' </'+self.tokenType+'>','')
            self.list_row_xml_after_JackTokenizer_idx += 1
    
    def append_state(self, desired_token = None):
        # Assume (self.token == desired_token) if (type(desired_token) == str)
        if (type(desired_token) == str) and (self.token != desired_token):
            print((type(desired_token) == str), (self.token != desired_token))
            print('-' + self.token + '-')
            print('-' + desired_token + '-')
            raise OurException('token ' + self.token + ' is not ' + desired_token + self.state_line())
        # Assume (self.token in desired_token) if (type(desired_token) == list)
        if (type(desired_token) == list) and (self.token not in desired_token):
            raise OurException('token ' + self.token + ' is not in ' + str(desired_token) + self.state_line())
        # Append and Update
        self.list_row_xml.append(self.row_xml_after_JackTokenizer)
        self.update_state()
    
    def state_line(self):
        return ', line ' + str(self.list_row_xml_after_JackTokenizer_idx + 1) + ', in ' + self.jack_name + 'T_ans.xml'
    
    def delimit_begin(self, token):
        self.list_row_xml.append('<' + token + '>')
    
    def delimit_end(self, token):
        self.list_row_xml.append('</' + token + '>')
    
    # --- Program structure ---

    def compileClass(self):
        # Delimit begin of class
        self.delimit_begin('class')
        # Append 'class'
        self.append_state('class')
        # Append className
        self.write_className()
        # Append '{'
        self.append_state('{')
        # Generate trees of classVarDec
        while self.token in ['static', 'field']:
            self.compileClassVarDec()
        # Generate trees of subroutineDec
        while self.token in ['constructor', 'function', 'method']:
            self.compileSubroutine()
        # Append '}'
        self.append_state('}')
        # Delimit end of class
        self.delimit_end('class')
    
    def compileClassVarDec(self):
        # Delimit begin of classVarDec
        self.delimit_begin('classVarDec')
        # Append 'static' or 'field'
        self.append_state(['static', 'field'])
        # Append type
        self.write_type()
        # Append varName
        self.write_varName()
        # Append ',' and varName if they still exist
        while self.token == ',':
            self.append_state(',') # ','
            self.write_varName() # varName
        # Append ';'
        self.append_state(';')
        # Delimit end of classVarDec
        self.delimit_end('classVarDec')
    
    def write_type(self):
        # Append type
        self.append_state()

    def compileSubroutine(self):
        # Delimit begin of subroutineDec
        self.delimit_begin('subroutineDec')
        # Append 'constructor', 'function', or 'method'
        self.append_state(['constructor', 'function', 'method'])
        # Append 'void' or type
        if self.token == 'void':
            self.append_state('void')
        else:
            self.write_type()
        # Append subroutineName
        self.write_subroutineName()
        # Append '('
        self.append_state('(')
        # Generate tree of parameterList
        self.compileParameterList()
        # Append ')'
        self.append_state(')')
        # Generate tree of subroutineBody
        self.compileSubroutineBody()
        # Delimit end of subroutineDec
        self.delimit_end('subroutineDec')

    def compileParameterList(self):
        # Delimit begin of parameterList
        self.delimit_begin('parameterList')
        # Append type if there exists
        if self.token != ')':
            self.write_type()
            # Append varName
            self.write_varName()
            # Append ',' if there still exist
            while self.token != ')':
                self.append_state(',')
                # Append type
                self.write_type()
                # Append varName
                self.write_varName()
        # Delimit end of parameterList
        self.delimit_end('parameterList')
    
    def compileSubroutineBody(self):
        # Delimit begin of subroutineBody
        self.delimit_begin('subroutineBody')
        # Append '{'
        self.append_state('{')
        # Generate trees of varDec if there still exist
        while self.token == 'var':
            self.compileVarDec()
        # Generate tree of statements
        self.compileStatements()
        # Append '}'
        self.append_state('}')
        # Delimit end of subroutineBody
        self.delimit_end('subroutineBody')
    
    def compileVarDec(self):
        # Delimit begin of varDec
        self.delimit_begin('varDec')
        # Append 'var'
        self.append_state('var')
        # Append type
        self.write_type()
        # Append varName
        self.write_varName()
        # Append ',' if there still exist
        while self.token == ',':
            self.append_state(',')
            # Append varName
            self.write_varName()
        # Append ';'
        self.append_state(';')
        # Delimit end of varDec
        self.delimit_end('varDec')
        
    def write_className(self):
        # Append className
        self.append_state()
    
    def write_subroutineName(self):
        # Append subroutineName
        self.append_state()
    
    def write_varName(self):
        # Append varName
        self.append_state()
    
    # --- statements ---

    def compileStatements(self):
        # Delimit begin of statements
        self.delimit_begin('statements')
        # Generate trees of *statement if there still exist
        while self.token != '}':
            if self.token == 'let':
                self.compileLet()
            elif self.token == 'if':
                self.compileIf()
            elif self.token == 'while':
                self.compileWhile()
            elif self.token == 'do':
                self.compileDo()
            elif self.token == 'return':
                self.compileReturn()
            else:
                raise OurException('token ' + self.token + ' is invalid at compileStatements()' + self.state_line())
        # Delimit end of statements
        self.delimit_end('statements')
    
    def compileLet(self):
        # Delimit begin of let
        self.delimit_begin('letStatement')
        # Append 'let'
        self.append_state('let')
        # Append varName
        self.write_varName()
        # Append '[' if there exist
        if self.token == '[':
            self.append_state('[')
            # Generate tree of expression
            self.compileExpression()
            # Append ']'
            self.append_state(']')
        # Append '='
        self.append_state('=')
        # Generate tree of expression
        self.compileExpression()
        # Append ';'
        self.append_state(';')
        # Delimit end of let
        self.delimit_end('letStatement')

    def compileIf(self):
        # Delimit begin of if
        self.delimit_begin('ifStatement')
        # Append 'if'
        self.append_state('if')
        # Append '('
        self.append_state('(')
        # Generate tree of expression
        self.compileExpression()
        # Append ')'
        self.append_state(')')
        # Append '{'
        self.append_state('{')
        # Generate tree of statements
        self.compileStatements()
        # Append '}'
        self.append_state('}')
        # Append 'else' if there exist
        if self.token == 'else':
            self.append_state('else')
            # Append '{'
            self.append_state('{')
            # Generate tree of statements
            self.compileStatements()
            # Append '}'
            self.append_state('}')
        # Delimit end of if
        self.delimit_end('ifStatement')

    def compileWhile(self):
        # Delimit begin of while
        self.delimit_begin('whileStatement')
        # Append 'while'
        self.append_state('while')
        # Append '('
        self.append_state('(')
        # Generate tree of expression
        self.compileExpression()
        # Append ')'
        self.append_state(')')
        # Append '{'
        self.append_state('{')
        # Generate tree of statements
        self.compileStatements()
        # Append '}'
        self.append_state('}')
        # Delimit end of while
        self.delimit_end('whileStatement')
    
    def compileDo(self):
        # Delimit begin of do
        self.delimit_begin('doStatement')
        # Append 'do'
        self.append_state('do')
        # Generate tree of subroutineCall
        self.write_subroutineCall()
        # Append ';'
        self.append_state(';')
        # Delimit end of do
        self.delimit_end('doStatement')
    
    def compileReturn(self):
        # Delimit begin of return
        self.delimit_begin('returnStatement')
        # Append 'return'
        self.append_state('return')
        # Generate trees of expression if there still exist
        while self.token != ';':
            self.compileExpression()
        # Append ';'
        self.append_state(';')
        # Delimit end of return
        self.delimit_end('returnStatement')

    # --- expression ---
    
    def compileExpression(self):
        # Delimit begin of expression
        self.delimit_begin('expression')
        # Generate tree of term
        self.compileTerm()
        # Append op if there still exist
        while self.token in self.LIST_OP:
            self.write_op()
            # Generate tree of term
            self.compileTerm()
        # Delimit end of expression
        self.delimit_end('expression')
    
    # compileTerm() in stage2_1 is only for ExpressionLess
    def compileTerm(self):
        # Delimit begin of term
        self.delimit_begin('term')
        # Append term with no conditions
        self.append_state()
        # Delimit end of term
        self.delimit_end('term')
    
    def write_subroutineCall(self):
        # Append subroutineName
        # It can be className or varName
        self.write_subroutineName()
        # Appen '.' if the former token is className or varName
        if self.token == '.':
            self.append_state('.')
            # Append subroutineName
            self.write_subroutineName()
        # Append '('
        self.append_state('(')
        # Generate tree of expressionList
        self.compileExpressionList()
        # Append ')'
        self.append_state(')')
    
    def compileExpressionList(self):
        # Delimit begin of expressionList
        self.delimit_begin('expressionList')
        # Generate tree of expression if there exist
        if self.token != ')':
            self.compileExpression()
            # Append ',' if there still exist
            while self.token != ')':
                self.append_state(',')
                # Generate tree of expression
                self.compileExpression()
        # Delimit end of expressionList
        self.delimit_end('expressionList')
    
    def write_op(self):
        # Append op
        self.append_state(self.LIST_OP)

class OurException(Exception):
    pass