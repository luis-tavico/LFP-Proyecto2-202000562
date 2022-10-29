class Token:

    def __init__(self, number, lexeme, type, line, column):
        self.number = number
        self.lexeme = lexeme
        self.type = type
        self.line = line
        self.column = column

    def getNumber(self):
        return self.number
    
    def getLexeme(self):
        return self.lexeme

    def getType(self):
        return self.type
    
    def getLine(self):
        return self.line

    def getColumn(self):
        return self.column

    def setNumber(self, number):
        self.number = number

    def setLexeme(self, lexeme):
        self.lexeme = lexeme

    def setType(self, type):
        self.type = type
    
    def setLine(self, line):
        self.line = line

    def setColumn(self, column):
        self.column = column