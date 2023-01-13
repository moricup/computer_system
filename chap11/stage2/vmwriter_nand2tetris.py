class VMWriter:
    def __init__(self, dir, jack_name, list_row_xml, dict_class_symbolTable, dict_dict_method_symbolTable):
        self.dir = dir
        self.jack_name = jack_name
        self.list_row_xml = list_row_xml
        self.dict_class_symbolTable = dict_class_symbolTable
        self.dict_dict_method_symbolTable = dict_dict_method_symbolTable
        # list of row_vm for output
        self.list_row_vm = []
        # index of list_row_xml
        self.idx_row_xml = -1
        # elements of row_xml
        self.tag = None
        self.token = None
        # elements of next row_xml
        self.tag_next = None
        self.token_next = None
        # index of label
        self.idx_label = 0

        # Update first row_xml
        self.update_row_xml()
        if self.tag != '<class>':
            raise OurException('tag ' + str(self.tag) + ' is not <class>' + self.state_line())
        # Start reading row_xml
        self.read_class()
    
    def output_list_row_vm(self):
        return self.list_row_vm
    
    def update_row_xml(self):
        # Increment idx_row_xml
        self.idx_row_xml += 1
        if self.idx_row_xml >= len(self.list_row_xml):
            raise OurException('idx_row_xml is exceeded.')
        
        # Get row_xml
        row_xml = self.list_row_xml[self.idx_row_xml]
        if len(row_xml.split(' ')) == 1: # This is a delimit-tag
            self.tag = row_xml.split(' ')[0]
            self.token = None
        else: # This is a token
            self.tag = row_xml.split(' ')[0]
            self.token = row_xml.replace(self.tag.replace('>','> '),'').replace(self.tag.replace('<',' </'), '')
        
        # Get row_xml_next
        if self.idx_row_xml + 1 < len(self.list_row_xml):
            row_xml_next = self.list_row_xml[self.idx_row_xml + 1]
            if len(row_xml_next.split(' ')) == 1: # This is a delimit-tag
                self.tag_next = row_xml_next.split(' ')[0]
                self.token_next = None
            else: # This is a token
                self.tag_next = row_xml_next.split(' ')[0]
                self.token_next = row_xml_next.replace(self.tag_next.replace('>','> '),'').replace(self.tag_next.replace('<',' </'),'')
        else:
            self.tag_next = None
            self.token_next = None
    
    def state_line(self):
        return ', line ' + str(self.idx_row_xml) + ', in ' + self.dir + '/' + self.jack_name + '.'
    
    def convert_segment(self, segment):
        if segment == 'field':
            segment = 'this'
        elif segment == 'var':
            segment = 'local'
        return segment
    
    def get_nLocals(self, dict_method_symbolTable):
        nLocals = 0
        for type_kind_index in dict_method_symbolTable.values():
            kind = type_kind_index[1]
            if kind == 'var':
                nLocals += 1
        return nLocals
    
    def get_type_kind_index(self, dict_method_symbolTable):
        if self.token in self.dict_class_symbolTable.keys():
            type_kind_index = self.dict_class_symbolTable[self.token]
        elif self.token in dict_method_symbolTable.keys():
            type_kind_index = dict_method_symbolTable[self.token]
        else:
            type_kind_index = [None,None,None]
        return type_kind_index
    
    def check_tag(self, desired_tag):
        if self.tag != desired_tag:
            raise OurException('tag ' + str(self.tag) + ' is not ' + desired_tag + self.state_line())
    
    def check_token(self, desired_token):
        if self.token != desired_token:
            raise OurException('token ' + str(self.token) + ' is not ' + desired_token + self.state_line())
    
    def raise_tag_token(self):
        raise OurException('tag ' + str(self.tag) + ' and token ' + str(self.token) + ' is invald' + self.state_line())

    # --- methods for writing ---

    def writePush(self, segment, index):
        segment = self.convert_segment(segment)
        self.list_row_vm.append('push ' + segment + ' ' + str(index))

    def writePop(self, segment, index):
        segment = self.convert_segment(segment)
        self.list_row_vm.append('pop ' + segment + ' ' + str(index))

    def writeArithmetic(self, command):
        self.list_row_vm.append(command)

    def writeLabel(self, label):
        self.list_row_vm.append('label ' + label)

    def writeGoto(self, label):
        self.list_row_vm.append('goto ' + label)

    def writeIf(self, label):
        self.list_row_vm.append('if-goto ' + label)

    def writeCall(self, name, nArgs):
        self.list_row_vm.append('call ' + name + ' ' + str(nArgs))

    def writeFunction(self, name, nLocals, kind):
        self.list_row_vm.append('function ' + self.jack_name + '.' + name + ' ' + str(nLocals))
        if kind == 'constructor':
            # Get num of fields
            nFields = 0
            for key_kind_index in self.dict_class_symbolTable.values():
                kind = key_kind_index[1]
                if kind == 'field':
                    nFields += 1
            # Call Memory.alloc
            self.writePush('constant', nFields)
            self.writeCall('Memory.alloc', 1)
            self.writePop('pointer', 0)
        elif kind == 'method':
            # Set this
            self.writePush('argument', 0)
            self.writePop('pointer', 0)

    def writeReturn(self):
        self.list_row_vm.append('return')
    
    def write_comment_tag(self, tag): # for visibility. We can pass it.
        #return
        self.list_row_vm.append('// ' + tag)
        pass
    
    def write_comment_begin(self, element_of_term): # for visibility. We can pass it.
        #return
        self.list_row_vm.append('// We begin reading ' + element_of_term)
        pass
    
    def write_comment_end(self, element_of_term): # for visibility. We can pass it.
        #return
        self.list_row_vm.append('// We end reading ' + element_of_term)
        pass
    
    def write_op(self, op):
        # Now, topmost two of stack are two arguments for op
        if op == '+':
            self.list_row_vm.append('add')
        elif op == '-':
            self.list_row_vm.append('sub')
        elif op == '*':
            self.writeCall('Math.multiply', 2)
        elif op == '/':
            self.writeCall('Math.divide', 2)
        elif op == '&amp;':
            self.list_row_vm.append('and')
        elif op == '|':
            self.list_row_vm.append('or')
        elif op == '&lt;':
            self.list_row_vm.append('lt')
        elif op == '&gt;':
            self.list_row_vm.append('gt')
        elif op == '=':
            self.list_row_vm.append('eq')
        else:
            raise OurException('op ' + str(op) + ' is invalid' + self.state_line())
    
    def write_unaryOp(self, unaryop):
        # Now, topmost of stack is to computed by unaryop
        if unaryop == '-':
            self.list_row_vm.append('neg')
        elif unaryop == '~':
            self.list_row_vm.append('not')
        else:
            raise OurException('unaryop ' + str(unaryop) + ' is invalid' + self.state_line())
    
    def write_not(self):
        self.list_row_vm.append('not')
    
    # --- methods for reading ---

    def read_class(self):
        # Write // <class>
        self.write_comment_tag(self.tag)
        
        while True:
            self.update_row_xml()
            if self.tag == '</class>': # This is end.
                break
            elif self.tag == '<subroutineDec>':
                self.read_subroutineDec()
        
        # Write // </class>
        self.write_comment_tag(self.tag)
    
    #def read_classVarDec(self):
    #    pass

    def read_subroutineDec(self):
        # Write // <subroutineDec>
        self.write_comment_tag(self.tag)

        self.update_row_xml() # Now token is kind
        if self.token not in ['constructor', 'function', 'method']:
            raise OurException('token ' + str(self.token) +' is not kind' + self.state_line())
        kind = self.token
        self.update_row_xml() # Now token is type
        self.update_row_xml() # Now token is subroutineName

        subroutineName = self.token
        # Get dict_method_symbolTable
        dict_method_symbolTable = self.dict_dict_method_symbolTable[subroutineName]
        # Get nLocals
        nLocals = self.get_nLocals(dict_method_symbolTable)
        # Write Function
        self.writeFunction(subroutineName, nLocals, kind)

        while True:
            self.update_row_xml()
            if self.tag == '</subroutineDec>':
                break
            elif self.tag == '<subroutineBody>':
                self.read_subroutineBody(dict_method_symbolTable)
        
        # Write // </subroutineDec>
        self.write_comment_tag(self.tag)


    #def read_paramaterList(self):
    #    pass

    def read_subroutineBody(self, dict_method_symbolTable):
        # Write // <subroutineBody>
        self.write_comment_tag(self.tag)

        while True:
            self.update_row_xml()
            if self.tag == '</subroutineBody>':
                break
            elif self.tag == '<statements>':
                self.read_statements(dict_method_symbolTable)
        
        # Write // </subroutineBody>
        self.write_comment_tag(self.tag)

    #def read_varDec(self):
    #    pass

    def read_statements(self, dict_method_symbolTable):
        # Write // <statements>
        self.write_comment_tag(self.tag)

        while True:
            self.update_row_xml()
            if self.tag == '</statements>':
                break
            elif self.tag == '<whileStatement>':
                self.read_whileStatement(dict_method_symbolTable)
            elif self.tag == '<ifStatement>':
                self.read_ifStatement(dict_method_symbolTable)
            elif self.tag == '<returnStatement>':
                self.read_returnStatement(dict_method_symbolTable)
            elif self.tag == '<letStatement>':
                self.read_letStatement(dict_method_symbolTable)
            elif self.tag == '<doStatement>':
                self.read_doStatement(dict_method_symbolTable)
        
        # Write // </statements>
        self.write_comment_tag(self.tag)

    def read_whileStatement(self, dict_method_symbolTable):
        # Write // <whileStatement>
        self.write_comment_tag(self.tag)

        # Define labels
        label_while_begin = 'WHILE_BEGIN' + str(self.idx_label)
        label_while_end = 'WHILE_END' + str(self.idx_label)
        self.idx_label += 1

        # Write label_while_begin
        self.writeLabel(label_while_begin)

        self.update_row_xml() # This token is 'while'
        self.check_token('while')

        self.update_row_xml() # This token is '('
        self.check_token('(')

        self.update_row_xml() # This tag is <expression>
        self.check_tag('<expression>')
        self.read_expression(dict_method_symbolTable)

        self.update_row_xml() # This token is ')'
        self.check_token(')')
        
        # Now, topmost of stack is boolean for while-condition.
        # If False, then goto label_while_end
        self.write_not()
        self.writeIf(label_while_end)
        
        self.update_row_xml() # This token is '{'
        self.check_token('{')
        
        self.update_row_xml() # This tag is '<statements>'
        self.check_tag('<statements>')
        self.read_statements(dict_method_symbolTable)
        
        self.update_row_xml() # This token is '}'
        self.check_token('}')
        
        self.update_row_xml() # This tag is '</statements>'
        self.check_tag('</whileStatement>')

        # Go to label_while_begin
        self.writeGoto(label_while_begin)

        # Write label_while_end
        self.writeLabel(label_while_end)

        # Write // </whileStatement>
        self.write_comment_tag(self.tag)

    def read_ifStatement(self, dict_method_symbolTable):
        # Write // <ifStatement>
        self.write_comment_tag(self.tag)

        # Define lables
        label_else_begin = 'ELSE_BEGIN' + str(self.idx_label)
        label_else_end = 'ELSE_END' + str(self.idx_label)
        self.idx_label += 1

        self.update_row_xml() # This token is 'if'
        self.check_token('if')

        self.update_row_xml() # This token is '('
        self.check_token('(')
        
        self.update_row_xml() # This tag is <expression>
        self.check_tag('<expression>')
        self.read_expression(dict_method_symbolTable)

        self.update_row_xml() # This token is ')'
        self.check_token(')')
        
        # Now, topmost of stack is boolean for if-condition.
        # If False, then goto label_else_begin
        self.write_unaryOp('~') # Reverses the condition to determine either we go to 'else' or not.
        self.writeIf(label_else_begin)
        
        self.update_row_xml() # This token is '{'
        self.check_token('{')
        
        self.update_row_xml() # This tag is '<statements>'
        self.check_tag('<statements>')
        self.read_statements(dict_method_symbolTable)
        
        self.update_row_xml() # This token is '}'
        self.check_token('}')
        
        # Now, we are in end of if-True statements
        # Go to end of else statements 
        self.writeGoto(label_else_end)
        
        # Write label_else_begin
        self.writeLabel(label_else_begin)

        self.update_row_xml()
        if self.tag == '</ifStatement>': # This is end of ifStatement
            pass
        elif self.token == 'else': # There is else-statements
            self.update_row_xml() # This token is '{'
            self.check_token('{')
        
            self.update_row_xml() # This tag is '<statements>'
            self.check_tag('<statements>')
            self.read_statements(dict_method_symbolTable)
        
            self.update_row_xml() # This token is '}'
            self.check_token('}')
            
            self.update_row_xml() # This tag is </ifStatement>
            self.check_tag('</ifStatement>')
        else:
            self.raise_tag_token()

        # Write label_else_end
        self.writeLabel(label_else_end)

        # Write // </ifStatement>
        self.write_comment_tag(self.tag)

    def read_returnStatement(self, dict_method_symbolTable):
        # Write // <returnStatement>
        self.write_comment_tag(self.tag)

        self.update_row_xml() # This is 'return'
        self.check_token('return')

        self.update_row_xml()
        if self.token == ';':
            pass
        elif self.tag == '<expression>':
            self.read_expression(dict_method_symbolTable)

            self.update_row_xml() # This token is ';'
            self.check_token(';')
        else:
            self.raise_tag_token()
        
        # Write return
        self.writeReturn()

        self.update_row_xml() # This tag is </returnStatement>
        self.check_tag('</returnStatement>')

        # Write // </returnStatement>
        self.write_comment_tag(self.tag)

    def read_letStatement(self, dict_method_symbolTable):
        # Write // <letStatement>
        self.write_comment_tag(self.tag)

        self.update_row_xml() # This token is 'let'
        self.check_token('let')

        self.update_row_xml() # This token is varName
        varName = self.token

        # Get kind, index of varName
        _, kind, index = self.get_type_kind_index(dict_method_symbolTable)
        if kind == None:
            raise OurException('varName ' + varName + ' is invalid in read_letStatement()' + self.state_line())

        self.update_row_xml() # This is '[' or '='

        if self.token == '[': # The destination of pop is Array
            is_the_destination_of_pop_Array = True

            # Push varName of varName[expression]
            self.writePush(kind, index)

            self.update_row_xml() # This tag is '<expression>'
            self.check_tag('<expression>')
            self.read_expression(dict_method_symbolTable)

            # Now, topmost two of stack is address of varName and expression in varName[expression] (expression is top)
            # Then the sum of them is address of varName[expression]
            self.write_op('+')

            self.update_row_xml() # This token is ']'
            self.check_token(']')

            self.update_row_xml() # This token is '='

        else: # The destination of pop is varName
            is_the_destination_of_pop_Array = False

        # Now token is '='
        self.check_token('=')

        self.update_row_xml() # This tag is <expression>
        self.check_tag('<expression>')
        self.read_expression(dict_method_symbolTable)

        if is_the_destination_of_pop_Array == True:
            # Now, topmost two of stack are address of varName[expression] and expression (expression is top)
            # We assign expression to varName[expression]
            self.writePop('temp', 0)
            self.writePop('pointer', 1)
            self.writePush('temp', 0)
            self.writePop('that', 0)
        else:
            # Now, topmost of stack is expression
            # Moreover, we know kind and index of varName to be assigned
            # We assign expression to varName
            self.writePop(kind, index)

        self.update_row_xml() # This token is ';'
        self.check_token(';')

        self.update_row_xml() # This tag is </letStatement>
        self.check_tag('</letStatement>')

        # Write // </letStatement>
        self.write_comment_tag(self.tag)

    def read_doStatement(self, dict_method_symbolTable):
        # Write // <doStatement>
        self.write_comment_tag(self.tag)

        self.update_row_xml() # This token is 'do'
        self.check_token('do')

        self.update_row_xml()
        # We are in top of subroutineCall without tag
        self.read_subroutineCall(dict_method_symbolTable)

        # Drop return value
        self.writePop('temp', 0)

        self.update_row_xml() # This token is ';'
        self.check_token(';')

        self.update_row_xml() # This tag is </doStatement>
        self.check_tag('</doStatement>')

        # Write // </doStatement>
        self.write_comment_tag(self.tag)

    def read_expression(self, dict_method_symbolTable):
        # Write // <expression>
        self.write_comment_tag(self.tag)

        self.update_row_xml() # This tag is <term>
        if self.tag != '<term>':
            raise OurException('tag ' + self.tag + ' is not <term>' + self.state_line())
        self.read_term(dict_method_symbolTable)

        # Now, topmost of stack is term

        while True:
            self.update_row_xml()
            if self.tag == '</expression>': # This is end of expression
                break
            elif self.tag == '<symbol>': # This token is op
                op = self.token

                self.update_row_xml() # This tag is <term>
                self.check_tag('<term>')
                self.read_term(dict_method_symbolTable)

                # Now, topmost two of stack are two arguments for op
                # Write op
                self.write_op(op)
            else:
                raise OurException('tag ' + self.tag + ' is invalid' + self.state_line())
            

        # Now, topmost of stack is expression

        # Write // </expression>
        self.write_comment_tag(self.tag)

    def read_term(self, dict_method_symbolTable):
        # Write // <term>
        self.write_comment_tag(self.tag)

        self.update_row_xml()
        if self.tag == '<integerConstant>':
            self.read_integerConstant()
        elif self.tag == '<stringConstant>':
            self.read_stringConstant()
        elif self.token in ['true', 'false', 'null', 'this']:
            self.read_keywordConstant()
        elif self.token_next == '[':
            self.read_varNameArray(dict_method_symbolTable)
        elif self.token_next == '(' or self.token_next == '.':
            self.read_subroutineCall(dict_method_symbolTable)
        elif self.token == '(':
            self.read_braketExpression(dict_method_symbolTable)
        elif self.token in ['-', '~']:
            self.read_unaryOpTerm(dict_method_symbolTable)
        elif self.tag == '<identifier>':
            self.read_varName(dict_method_symbolTable)
        else:
            self.raise_tag_token()
        
        self.update_row_xml() # This tag is </term>
        self.check_tag('</term>')

        # Write // </term>
        self.write_comment_tag(self.tag)
    
    def read_integerConstant(self):
        # We are in top of subroutineCall without tag
        # Write begining
        self.write_comment_begin('integerConstant')

        # Push integerConstant
        self.writePush('constant', self.token)

        # Write ending
        self.write_comment_end('integerConstant')

    def read_stringConstant(self):
        # We are in top of subroutineCall without tag
        # Write begining
        self.write_comment_begin('stringConstant')

        # Get length of string
        maxLength = len(self.token)

        # Push maxLength which is arg of String.new()
        self.writePush('constant', maxLength)

        # Call String.new()
        self.writeCall('String.new', 1)

        # Append all char
        for char_of_token in self.token:
            self.writePush('constant', ord(char_of_token))
            self.writeCall('String.appendChar', 2)

        # Write ending
        self.write_comment_end('stringConstant')

    def read_keywordConstant(self):
        # We are in top of subroutineCall without tag
        # Write begining
        self.write_comment_begin('keywordConstant')

        if self.token == 'true':
            self.writePush('constant', 0)
            self.write_unaryOp('~')
        elif self.token == 'false':
            self.writePush('constant', 0)
        elif self.token == 'null':
            self.writePush('constant', 0)
        elif self.token == 'this':
            self.writePush('pointer', 0)
        else:
            raise OurException('token ' + self.token + ' is invalid in read_keywordConstant()' + self.state_line())

        # Write ending
        self.write_comment_end('keywordConstant')

    def read_varName(self, dict_method_symbolTable):
        # We are in top of subroutineCall without tag
        # Write begining
        self.write_comment_begin('varName')

        # Push
        _, kind, index = self.get_type_kind_index(dict_method_symbolTable)
        if kind == None:
            raise OurException('token ' + self.token + ' is invalid' + self.state_line())
        self.writePush(kind, index)

        # Write ending
        self.write_comment_end('varName')

    def read_varNameArray(self, dict_method_symbolTable):
        # We are in top of subroutineCall without tag
        # Write begining
        self.write_comment_begin('varNameArray')

        # Push varName
        varName = self.token
        _, kind, index = self.get_type_kind_index(dict_method_symbolTable)
        if kind == None:
            raise OurException('varName ' + varName + ' is invalid in read_varNameArray()' + self.state_line())
        self.writePush(kind, index)

        # Now, topmost of stack is the base address of varName which is an array.

        self.update_row_xml() # This token is '['
        self.check_token('[')

        self.update_row_xml() # This tag is <expression>
        self.check_tag('<expression>')
        self.read_expression(dict_method_symbolTable)

        # Now, topmost of stack is index of the array varName

        self.update_row_xml() # This token is ']'
        self.check_token(']')

        # After '+', topmost of stack is address of varName[expression]
        self.write_op('+')
        # After 'pop pointer 1', the address of 'that' is equal to the address of varName[expression]
        self.writePop('pointer', 1)
        # After 'push that 0', topmost of stack is varName[expression]
        self.writePush('that', 0)

        # Write ending
        self.write_comment_end('varNameArray')

    def read_subroutineCall(self, dict_method_symbolTable):
        # We are in top of subroutineCall without tag
        # Write begining
        self.write_comment_begin('subroutineCall')

        # Define counta of nArgs
        counta = Counta_nArgs()

        type, kind, index = self.get_type_kind_index(dict_method_symbolTable)
        if kind != None: # This subroutine is method
            # Push varName of varName.subroutineName()
            self.writePush(kind, index)
            # Add counta for 'this'
            counta.nArgs += 1
            # First name of subroutineName is type
            subroutineName = type
        else:
            # First name of subroutineName is subroutineName in subroutineName() or className in className.subroutineName()
            # i.e. The name is now token
            subroutineName = self.token
        
        self.update_row_xml() # This is '.' or '('
        if self.token == '.':
            subroutineName += '.'
            self.update_row_xml() # This is subroutineName in (className|varName).subroutineName()
            subroutineName += self.token
            self.update_row_xml() # This is '('
        else:
            # Now, we are reading subroutineName().
            # The kind is 'method'.
            # Then this is called as jack_name+'.'+subroutineName() whose 0-th argument is 'this'.
            subroutineName = self.jack_name + '.' + subroutineName
            # Push 'this'
            self.writePush('pointer', 0)
            # Add counta for 'this'
            counta.nArgs += 1
            pass
        self.check_token('(')
        
        self.update_row_xml() # This tag is <expressionList>
        self.check_tag('<expressionList>')
        self.read_expressionList(dict_method_symbolTable, counta)

        self.update_row_xml() # This token is ')'
        self.check_token(')')

        # Write Call
        self.writeCall(subroutineName, counta.nArgs)

        # Write ending
        self.write_comment_end('subroutineCall')

    def read_braketExpression(self, dict_method_symbolTable):
        # We are in top of subroutineCall without tag
        # Write begining
        self.write_comment_begin('braketExpression')

        self.update_row_xml() # This tag is <expression>
        self.check_tag('<expression>')
        self.read_expression(dict_method_symbolTable)

        self.update_row_xml() # This token is ')'
        self.check_token(')')

        # Write ending
        self.write_comment_end('braketExpression')

    def read_unaryOpTerm(self, dict_method_symbolTable):
        # We are in top of subroutineCall without tag
        # Write begining
        self.write_comment_begin('unaryOpTerm')

        # Get unaryop
        unaryop = self.token

        self.update_row_xml() # This tag is <term>
        self.check_tag('<term>')
        self.read_term(dict_method_symbolTable)

        # Now, topmost of stack is argument for unaryOp
        # Write unaryOp
        self.write_unaryOp(unaryop)

        # Write ending
        self.write_comment_end('unaryOpTerm')

    def read_expressionList(self, dict_method_symbolTable, counta = None):
        # Write // <expressionList>
        self.write_comment_tag(self.tag)

        self.update_row_xml()
        if self.tag == '</expressionList>': # There are no expressions
            pass
        elif self.tag == '<expression>': # There are expressions
            if counta != None: # Add counta
                counta.nArgs += 1
            self.read_expression(dict_method_symbolTable)
            while True:
                self.update_row_xml()
                if self.tag == '</expressionList>': # There are no more expressions
                    break
                
                if counta != None: # Add counta since there are more expressions
                    counta.nArgs += 1

                self.check_token(',') # This token is ',' because there are more expressions

                self.update_row_xml() # This tag is <expression>
                self.check_tag('<expression>')
                self.read_expression(dict_method_symbolTable)
        else:
            raise OurException('tag ' + self.tag + ' is neither </expressionList> nor <expression> ' + self.state_line())

        # Write // </expressionList>
        self.write_comment_tag(self.tag)

class Counta_nArgs:
    def __init__(self):
        self.nArgs = 0

class OurException(Exception):
    pass