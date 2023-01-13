class SymbolTable:
    def __init__(self, jack_name, list_row_xml):
        self.jack_name = jack_name
        self.list_row_xml = list_row_xml
        # dict for output
        # each element of dict is dict[identifier] = [type, kind, index]
        self.dict_class_symbolTable = {}
        # each element of dict_dict is dict[method_name] = dict_method_symbolTable
        self.dict_dict_method_symbolTable = {}
        # indexes
        self.list_row_xml_idx = -1
        self.static_idx = 0
        self.field_idx = 0
        self.argument_idx = 0
        self.var_idx = 0
        # Initialize all tables
        self.initialize_all_symbolTables()
    
    def output(self):
        return self.dict_class_symbolTable, self.dict_dict_method_symbolTable

    def state_line(self):
        return ', line ' + str(self.list_row_xml_idx) +', in ' + self.jack_name + '_ans.xml'
    
    def get_next_token(self):
        while (self.list_row_xml_idx + 1) < len(self.list_row_xml): # See next row if there exists
            self.list_row_xml_idx += 1
            row_xml = self.list_row_xml[self.list_row_xml_idx]
            if len(row_xml.split(' '))==1: # Dismiss delimit-tag
                continue
            # There is a token.
            tokenType = row_xml.split(' ')[0].replace('<','').replace('>','')
            token = row_xml.replace('<'+tokenType+'> ','').replace(' </'+tokenType+'>','')
            return token
        # There are no tokens.
        return None
    
    def initialize_all_symbolTables(self):
        while (self.list_row_xml_idx + 1) < len(self.list_row_xml): # See next row if there exists.
            # Get token
            token = self.get_next_token()
            if (token == 'static') or (token == 'field'): # static or field should been appended.
                kind = token
                type = self.get_next_token()
                self.append_dict_class_symbolTable(kind, type)
            elif (token == 'constructor') or (token == 'function') or (token == 'method'):
                if token == 'method':
                    ismethod = True
                else:
                    ismethod = False
                _ = self.get_next_token() # This is type of the method.
                method_name = self.get_next_token()
                self.initialize_one_method_symbolTable(method_name, ismethod)
    
    def append_dict_class_symbolTable(self, kind, type):
        # Get identifier
        identifier = self.get_next_token()
        # Get index
        if kind == 'static':
            index = self.static_idx
            self.static_idx += 1
        elif kind == 'field':
            index = self.field_idx
            self.field_idx += 1
        else:
            raise OurException('kind ' + kind + ' is invalid in append_dict_class_symbolTable()' + self.state_line())
        # Append the element.
        self.dict_class_symbolTable[identifier] = [type, kind, index]
        # Get next token
        token = self.get_next_token()
        if token == ',': # Append more if next token is also identifier
            self.append_dict_class_symbolTable(kind, type)
    
    def initialize_one_method_symbolTable(self, method_name, ismethod):
        # Generate dict
        dict_method_symbolTable = {}
        if ismethod == True: # Append this
            dict_method_symbolTable['this'] = [self.jack_name, 'argument', self.argument_idx]
            # increment
            self.argument_idx += 1
        # Get token
        token = self.get_next_token()
        if token != '(': # This token should be '('
            raise OurException('token ' + token + ' is invalid in initialize_one_method_table()' + self.state_line())
        # Append arguments if there exist
        self.append_argument_to_dict_method_symbolTable(dict_method_symbolTable)
        while (self.list_row_xml_idx + 1) < len(self.list_row_xml): # See next row if there exists.
            # Get token
            token = self.get_next_token()
            if token == 'return': # We are almost end of method.
                break
            if token == 'var': # var should be appended
                type = self.get_next_token()
                self.append_var_to_dict_method_symbolTable(dict_method_symbolTable, type)
        # Append dict
        self.dict_dict_method_symbolTable[method_name] = dict_method_symbolTable
        # Reset indexes
        self.argument_idx = 0
        self.var_idx = 0
    
    def append_argument_to_dict_method_symbolTable(self, dict_method_symbolTable):
        # Get token
        token = self.get_next_token()
        # Assume token != None
        if token == None:
            raise OurException('token in append_argument_to_dict_method_symbolTable() is None.')
        if token != ')': # There is argument
            if token == ',': # We are in not first argument
                token = self.get_next_token()
            # Now token is type
            type = token
            # Next token is identifier
            identifier = self.get_next_token()
            # Append the element
            dict_method_symbolTable[identifier] = [type, 'argument', self.argument_idx]
            # increment
            self.argument_idx += 1
            # Append more arguments if there exist
            self.append_argument_to_dict_method_symbolTable(dict_method_symbolTable)
    
    def append_var_to_dict_method_symbolTable(self, dict_method_symbolTable, type):
        # Get identifier
        identifier = self.get_next_token()
        # Append the element.
        dict_method_symbolTable[identifier] = [type, 'var', self.var_idx]
        # increment
        self.var_idx += 1
        # Get next token
        token = self.get_next_token()
        if token == ',': # Append more if next token is also identifier
            self.append_var_to_dict_method_symbolTable(dict_method_symbolTable, type)

class OurException(Exception):
    pass