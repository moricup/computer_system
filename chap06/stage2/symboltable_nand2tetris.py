class SymbolTable:
    def __init__(self):
        self.table = {}
        self.address = 16
    
    def addEntry(self, symbol): # use to memorize address of symbol
        self.table[symbol] = format(self.address, 'b').zfill(15)
        self.address += 1
    
    def contains(self, symbol):
        return symbol in self.table.keys()
    
    def getAddress(self, symbol):
        return self.table[symbol]