class JackTokenizer:
    def __init__(self, jack):
        # list of jack_row without new-line, W-slash-comment, and tab
        self.jack = [jack_row.replace('\n', '').split('//')[0].replace('\t', '') for jack_row in jack.readlines()]
        # now_row_idx in jack which satisfies self.jack_row == self.jack[self.now_row_idx]
        self.now_row_idx = 0
        self.jack_row = ''
        # now_char_idx in self.jack_row which satisfies self.jack_char == self.jack_row[self.now_char_idx]
        self.now_char_idx = 0
        self.jack_char = ''
        # variable for memorizing to read comments
        self.now_comments = False
        # variables for setting self.token = self.jack_row[self.check_char_idx : self.now_char_idx]
        self.check_char_idx = 0
        self.token = ''
        # lists of researved notation
        self.LIST_KEYWORD = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self.LIST_SYMBOL = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def hasMoreTokens(self):
        while(self.now_row_idx < len(self.jack)):
            # Set self.jack_row
            self.jack_row = self.jack[self.now_row_idx]

            # Continue if we are reading comments
            if '*/' in self.jack_row:
                self.now_comments = False
                self.now_row_idx += 1
                continue
            if self.now_comments == True:
                self.now_row_idx += 1
                continue
            if '/*' in self.jack_row:
                self.now_comments = True
                continue

            # Start reading self.jack_row char by char.
            while(self.now_char_idx < len(self.jack_row)):
                # Set self.jack_char
                self.jack_char = self.jack_row[self.now_char_idx]

                # Continue if we are reading ' '(blank)
                if self.jack_char == ' ':
                    self.now_char_idx += 1
                    continue

                # Save self.token if self.jack_char is SYMBOL
                if self.jack_char in self.LIST_SYMBOL:
                    self.token = self.jack_char
                    # In next time, we read next char.
                    self.now_char_idx += 1
                    # Return True because there is a token.
                    return True

                # Fix self.check_char_idx because we are reading something which is not ' '(blank) and SYMBOL.
                self.check_char_idx = self.now_char_idx
                # Shift next char.
                self.now_char_idx = self.now_char_idx + 1

                # Start next reading self.jack_row from (self.check_char_idx + 1) which is STRING_CONST.
                if self.jack_row[self.check_char_idx] == '"':
                    while(self.now_char_idx < len(self.jack_row)):
                        # Set self.jack_char
                        self.jack_char = self.jack_row[self.now_char_idx]

                        # This is end of token if we are reading '"'..
                        if self.jack_char == '"':
                            # In next loop, we begin reading at NEXT char.
                            self.now_char_idx += 1
                            break

                        # Shift next char.
                        self.now_char_idx += 1

                # Start next reading self.jack_row from (self.check_char_idx + 1) which is NOT STRING_CONST.
                else:
                    while(self.now_char_idx < len(self.jack_row)):
                        # Set self.jack_char
                        self.jack_char = self.jack_row[self.now_char_idx]

                        # This is end of token if we are reading ' '(blank) or SYMBOL.
                        if self.jack_char == ' ' or self.jack_char in self.LIST_SYMBOL:
                            # In next loop, we begin reading at NOW char.
                            break

                        # Shift next char.
                        self.now_char_idx += 1
                
                # Save self.token
                self.token = self.jack_row[self.check_char_idx: self.now_char_idx]
                # Return True because there is a token.
                return True 

            # Shift next row.
            self.now_row_idx += 1
            self.now_char_idx = 0

        # Return False
        # Because there is not token.
        return False
    
    def tokenType(self):
        if self.token in self.LIST_KEYWORD:
            return 'KEYWORD'
        elif self.token in self.LIST_SYMBOL:
            return 'SYMBOL'
        elif self.token[0].isnumeric():
            return 'INT_CONST'
        elif self.token[0] == '"':
            return 'STRING_CONST'
        else:
            return 'IDENTIFIER'
    
    def keyWord(self):
        return self.token.upper()
    
    def symbol(self):
        return self.token
    
    def identifier(self):
        return self.token
    
    def intVal(self):
        return self.token
    
    def stringVal(self):
        return self.token.replace('"', '')

class OurException(Exception):
    pass