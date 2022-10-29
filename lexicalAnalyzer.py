from modelToken import Token
from modelError import Error

class LexicalAnalyzer:
    def __init__(self):
        self.errores = []
        self.tokens = []
        """self.tokensReservados = ["Controles", "Etiqueta", "Boton", "Check", "RadioBoton", "Texto", "AreaTexto", "Clave", "Contenedor", 
                                "propiedades", "setColorLetra", "setTexto", "setAlineacion", "setColorFondo", "setMarcada", "setGrupo", "setAncho", "setAlto",
                                "Colocacion", "setPosicion", "add"]"""

        self.tokensLabel = ["Controles", "propiedades", "Colocacion"]
        self.tokensType = ["Etiqueta", "Boton", "Check", "RadioBoton", "Texto", "AreaTexto", "Clave", "Contenedor"]     
        self.tokensProperty= ["setColorLetra", "setTexto", "setAlineacion", "setColorFondo", "setMarcada", "setGrupo", "setAncho", "setAlto", "setPosicion", "add"]    
        self.numLine = 1 
        self.numColumn = 0
        self.numError = 0
        self.numToken = 0
        self.scanner = ""
        self.state = 0 #initial State 
        self.i = 0 
        self.lineComment = False
        self.multilineComment = False

    def addToken(self, lexeme, type, numLinea, numColumna):
        if self.lineComment == False and self.multilineComment == False:
            self.numToken += 1
            self.tokens.append(Token(self.numToken, lexeme, type, numLinea, numColumna)) 
        self.scanner = ""

    def addError(self, lexeme, numLine, numColumn):
        self.errores.append(Error(lexeme, "Lexico", numLine, numColumn, "Token no esperado", f'Se obtuvo token "{ lexeme }" no esperado.'))

    def s0(self, lexeme:str):
        #ESTADO S0
        if lexeme.isalpha() or lexeme.isdigit():
            self.state = 1
            self.scanner += lexeme
            self.numColumn += 1
        elif lexeme == '<':
            self.state = 2
            self.scanner += lexeme
            self.numColumn +=1
        elif lexeme == '!':
            self.state = 3
            self.scanner += lexeme
            self.numColumn +=1
        elif lexeme == "-":
            self.state = 4
            self.scanner += lexeme
            self.numColumn +=1 
        elif lexeme == '/':
            self.state = 5
            self.scanner += lexeme
            self.numColumn +=1
        elif lexeme == "*":
            self.state = 6
            self.scanner += lexeme
            self.numColumn +=1 
        elif lexeme == ".":
            self.state = 7
            self.scanner += lexeme
            self.numColumn +=1
        elif lexeme == ",":
            self.state = 8
            self.scanner += lexeme
            self.numColumn +=1
        elif lexeme == ";":
            self.state = 9
            self.scanner += lexeme
            self.numColumn +=1
        elif lexeme == '(':
            self.state = 10
            self.scanner += lexeme
            self.numColumn +=1
        elif lexeme == '"':
            self.state = 11
            self.scanner += lexeme
            self.numColumn +=1
        elif lexeme == ')':
            self.state = 12
            self.scanner += lexeme
            self.numColumn +=1
        elif lexeme == '>':
            self.state = 13
            self.scanner += lexeme
            self.numColumn +=1
        elif lexeme == '\n':
            self.lineComment = False
            self.numColumn = 0
            self.numLine += 1
        elif lexeme in ["\t"," "]:
            self.numColumn += 1
        else:
            self.numColumn += 1           
            if self.lineComment == False and self.multilineComment == False:
                self.numError += 1
                self.addError(lexeme, self.numLine, self.numColumn)  
            
    def s1(self,lexeme:str):
        #State S1
        if lexeme.isalpha():
            self.state = 1
            self.scanner += lexeme
            self.numColumn += 1
        elif lexeme.isdigit():
            self.state = 1
            self.scanner += lexeme
            self.numColumn += 1  
        elif lexeme == "." and self.scanner.isdigit():
            self.state = 1
            self.scanner += lexeme
            self.numColumn += 1  
        else:
            numColumn = str(self.numColumn - (len(self.scanner)-1))
            if self.scanner in self.tokensLabel:
                self.addToken(self.scanner, "tr_{}".format("Etiqueta"), self.numLine, numColumn)
            elif self.scanner in self.tokensType:
                self.addToken(self.scanner, "tr_{}".format("Tipo"), self.numLine, numColumn)
            elif self.scanner in self.tokensProperty:
                self.addToken(self.scanner, "tr_{}".format("Propiedad"), self.numLine, numColumn)
            else:
                self.addToken(self.scanner, "Contenido", self.numLine, numColumn)
            self.state = 0
            self.i -= 1

    def s2(self):
        #State S2
        self.addToken(self.scanner, "tr_MenorQue", self.numLine, self.numColumn)
        self.state = 0
        self.i -= 1

    def s3(self):
        #State S3
        self.addToken(self.scanner, "tr_ExclamacionCerrado", self.numLine, self.numColumn)
        self.state = 0
        self.i -= 1

    def s4(self):
        #State S4
        self.addToken(self.scanner, "tr_Guion", self.numLine, self.numColumn)
        self.state = 0
        self.i -= 1

    def s5(self,lexeme:str):
        #State S5
        if lexeme == "/":
            self.state = 5
            self.scanner += lexeme
            self.numColumn += 1
        elif lexeme == "*":
            self.state = 5
            self.scanner += lexeme
            self.numColumn += 1
        else:
            if self.scanner == "//":
                numColumn = str(self.numColumn - (len(self.scanner)-1))
                self.lineComment = True
                self.addToken(self.scanner, "pr_{}".format("Comentario"), self.numLine, numColumn)
            elif self.scanner == "/*":
                numColumn = str(self.numColumn - (len(self.scanner)-1))
                self.multilineComment = True
                self.addToken(self.scanner, "pr_{}".format("Comentario"), self.numLine, numColumn)
            else:
                self.addToken(self.scanner, "tr_BarraDiagonal", self.numLine, self.numColumn)
            self.state = 0
            self.i -= 1

    def s6(self,lexeme:str):
        #State S6
        if lexeme == "/":
            self.state = 6
            self.scanner += lexeme
            self.numColumn += 1
        else:
            if self.scanner == "*/":
                numColumn = str(self.numColumn - (len(self.scanner)-1))
                self.addToken(self.scanner, "pr_{}".format("Comentario"), self.numLine, numColumn)
                self.multilineComment = False
            else:
                self.addToken(self.scanner, "tr_Asterisco", self.numLine, self.numColumn)
            self.state = 0
            self.i -= 1

    def s7(self):
        #State S7
        self.addToken(self.scanner, "tr_Punto", self.numLine, self.numColumn)
        self.state = 0
        self.i -= 1

    def s8(self):
        #State S8
        self.addToken(self.scanner, "tr_Coma", self.numLine, self.numColumn)
        self.state = 0
        self.i -= 1
        
    def s9(self):
        #State S9
        self.addToken(self.scanner, "tr_PuntoYComa", self.numLine, self.numColumn)
        self.state = 0
        self.i -= 1

    def s10(self):
        #State S10
        self.addToken(self.scanner, "tr_ParentesisAbierto", self.numLine, self.numColumn)
        self.state = 0
        self.i -= 1

    def s11(self):
        #State S11
        self.addToken(self.scanner, "tr_ComillaDoble", self.numLine, self.numColumn)
        self.state = 0
        self.i -= 1
        
    def s12(self):
        #State S12
        self.addToken(self.scanner, "tr_ParentesisCerrado", self.numLine, self.numColumn)
        self.state = 0
        self.i -= 1

    def s13(self):
        #State S13
        self.addToken(self.scanner, "tr_MayorQue", self.numLine, self.numColumn)
        self.state = 0
        self.i -= 1
  
    def analyzer(self, content):
        content += ">"
        self.i = 0
        while self.i < len(content):
            if self.state == 0:
                self.s0(content[self.i])
            elif self.state == 1:
                self.s1(content[self.i])
            elif self.state == 2:
                self.s2()
            elif self.state == 3:
                self.s3()
            elif self.state == 4:
                self.s4()
            elif self.state == 5:
                self.s5(content[self.i])
            elif self.state == 6:
                self.s6(content[self.i])
            elif self.state == 7:
                self.s7()
            elif self.state == 8:
                self.s8()
            elif self.state == 9:
                self.s9()
            elif self.state == 10:
                self.s10()
            elif self.state == 11:
                self.s11()
            elif self.state == 12:
                self.s12()
            elif self.state == 13:
                self.s13()
            self.i += 1