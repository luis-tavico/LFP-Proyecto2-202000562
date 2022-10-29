class Error:

    def __init__(self,  lexeme, type, line, column, expected, description):
        self.lexeme = lexeme
        self.type = type
        self.line = line
        self.column = column
        self.expected = expected
        self.description = description
    
    def getLexeme(self):
        return self.lexeme

    def getType(self):
        return self.type

    def getLine(self):
        return self.line

    def getColumn(self):
        return self.column
    
    def getExpected(self):
        return self.expected

    def getDescription(self):
        return self.description

    def setLexeme(self, lexeme):
        self.lexeme = lexeme

    def setType(self, type):
        self.type = type

    def setLine(self, line):
        self.line = line

    def setColumn(self, column):
        self.column = column

    def setExpected(self, expected):
        self.expected = expected
    
    def setDescription(self, description):
        self.description = description