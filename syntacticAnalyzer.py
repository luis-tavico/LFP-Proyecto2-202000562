from lexicalAnalyzer import *
from modelError import Error

class SyntacticAnalyzer:

    def __init__(self, tokens):
        self.tokens = tokens
        self.errores = []
        self.variables = []
        self.position = 0

    def addError(self, lexeme, numLine, numColumn, expected, description):
        self.errores.append(Error(lexeme, "Sintactico", numLine, numColumn, expected, description))
            
    def observeToken(self, position):
        try:
            return self.tokens[position]
        except:
            return None
    
    def analyzer(self):
        self.start()

    def start(self):
        try:
            token = self.observeToken(self.position)
            if token.getType() == "tr_MenorQue":
                self.position += 1
                token = self.observeToken(self.position)
                if token.getType() == "tr_ExclamacionCerrado":
                    self.position += 1
                    token = self.observeToken(self.position)
                    if token.getType() == "tr_Guion":
                        self.position += 1
                        token = self.observeToken(self.position)
                        if token.getType() == "tr_Guion":
                            self.position += 1
                            token = self.observeToken(self.position)
                            if token.getType() == "tr_Etiqueta":
                                self.position += 1
                                if token.getLexeme() == "Controles":
                                    pos = 0
                                    token = self.observeToken(self.position)
                                    self.controls(token.getLine())                                 
                                elif token.getLexeme() == "propiedades":
                                    pos = 0
                                    self.properties_colocation(pos)       
                                elif token.getLexeme() == "Colocacion":
                                    pos = 0
                                    self.properties_colocation(pos)
                                token = self.observeToken(self.position)
                                if token.getType() == "tr_Etiqueta":
                                    self.position += 1
                                    token = self.observeToken(self.position)
                                    if token.getType() == "tr_Guion":
                                        self.position += 1
                                        token = self.observeToken(self.position)
                                        if token.getType() == "tr_Guion":
                                            self.position += 1
                                            token = self.observeToken(self.position)
                                            if token.getType() == "tr_MayorQue":
                                                self.position += 1
                                                self.start()
                                            else:
                                                self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_MayorQue", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                                                self.advance()
                                                self.start()
                                        else:
                                            self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_Guion", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                                            self.advance()
                                            self.start()
                                    else:
                                        self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_Guion", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                                        self.advance()
                                        self.start()
                                else:
                                    self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_Etiqueta", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                                    self.advance()
                                    self.start()
                            else:
                                self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_Etiqueta", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                                self.advance()
                                self.start()
                        else:
                            self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_Guion", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                            self.advance()
                            self.start()
                    else:
                        self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_Guion", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                        self.advance()
                        self.start()
                else:
                    self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_ExclamacionCerrado", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                    self.advance()
                    self.start()
            else:
                self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_MenorQue", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                self.advance()
                self.start()        
        except IndexError:
            return
        except AttributeError:
            return


    def controls(self, line):
        token = self.observeToken(self.position)
        if token.getType() == "tr_Etiqueta":
            return
        if token.getType() == "tr_Tipo" and token.getLine() == line:
            self.position += 1
            token = self.observeToken(self.position)
            if token.getType() == "Contenido" and token.getLine() == line:
                self.position += 1
                self.variables.append(token.getLexeme())
                token = self.observeToken(self.position)              
                if token.getType() == "tr_PuntoYComa" and token.getLine() == line:
                    self.position += 1
                    token = self.observeToken(self.position)
                    self.controls(token.getLine())
                else:
                    self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_PuntoYComa", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                    self.advancePositions(line)
                    token = self.observeToken(self.position)
                    self.controls(token.getLine())
            else:
                self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "Contenido", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                self.advancePositions(line)
                token = self.observeToken(self.position)
                self.controls(token.getLine())
        else:
            self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_Tipo", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
            self.advancePositions(line)
            token = self.observeToken(self.position)
            self.controls(token.getLine())
    
    def properties_colocation(self, pos):
        er_properties_colocation = ["Contenido", "tr_Punto", "tr_Propiedad", "tr_ParentesisAbierto",
                                    "tr_ParentesisCerrado", "tr_PuntoYComa"]
        token = self.observeToken(self.position)
        if token.getType() == "tr_Etiqueta":
            return
        if token.getType() == er_properties_colocation[pos] and token.getLexeme() in self.variables:
            self.position += 1
            pos += 1
            token = self.observeToken(self.position)
            if token.getType() == er_properties_colocation[pos]:
                self.position += 1
                pos += 1
                token = self.observeToken(self.position)
                if token.getType() == er_properties_colocation[pos]:
                    self.position += 1
                    pos += 1
                    lexeme = token.getLexeme()
                    token = self.observeToken(self.position)
                    if token.getType() == er_properties_colocation[pos]:
                        self.position += 1
                        pos += 1
                        if lexeme in ["setTexto", "setAlineacion", "setMarcada", "setGrupo", "add"]:
                            self.insideParenthesesLetters()
                        elif lexeme in ["setColorLetra", "setColorFondo", "setAncho", "setAlto", "setPosicion"]:
                            self.insideParenthesesNumbers()
                        token = self.observeToken(self.position)
                        if token.getType() == er_properties_colocation[pos]:
                            self.position += 1
                            pos += 1
                            token = self.observeToken(self.position)
                            if token.getType() == er_properties_colocation[pos]:
                                self.position += 1
                                pos = 0
                                self.properties_colocation(pos)
                            else:
                                self.addError(token.getLexeme(), token.getLine(), token.getColumn(), er_properties_colocation[pos], f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                                self.advancePositions(token.getLine())
                                pos = 0
                                self.properties_colocation(pos)
                        else:
                            self.addError(token.getLexeme(), token.getLine(), token.getColumn(), er_properties_colocation[pos], f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                            self.advancePositions(token.getLine())
                            pos = 0
                            self.properties_colocation(pos)
                    else:
                        self.addError(token.getLexeme(), token.getLine(), token.getColumn(), er_properties_colocation[pos], f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                        self.advancePositions(token.getLine())
                        pos = 0
                        self.properties_colocation(pos)
                else:
                    self.addError(token.getLexeme(), token.getLine(), token.getColumn(), er_properties_colocation[pos], f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                    self.advancePositions(token.getLine())
                    pos = 0
                    self.properties_colocation(pos)
            else:
                self.addError(token.getLexeme(), token.getLine(), token.getColumn(), er_properties_colocation[pos], f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                self.advancePositions(token.getLine())
                pos = 0
                self.properties_colocation(pos)
        else:
            if token.getType() == er_properties_colocation[pos]:
                self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "Contenido", f'La variable "{ token.getLexeme() }" no existe.')
            else:
                self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "Contenido", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
            self.advancePositions(token.getLine())
            pos = 0
            self.properties_colocation(pos)


    def insideParenthesesLetters(self):
        token = self.observeToken(self.position)
        if token.getType() == "tr_ComillaDoble":
            self.position += 1
            token = self.observeToken(self.position)
            if token.getType() == "Contenido":
                self.position += 1
                token = self.observeToken(self.position)
            if token.getType() == "tr_ComillaDoble":
                self.position += 1
            else:
                self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "tr_ComillaDoble", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                self.advancePositions(token.getLine())
                return
        elif token.getType() == "Contenido":
            self.position += 1
        else: 
            self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "Contenido", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
            self.advancePositions(token.getLine())
            return
        return 

    def insideParenthesesNumbers(self):
        token = self.observeToken(self.position)
        if token.getType() == "Contenido":
            self.position += 1
            token = self.observeToken(self.position)
            if token.getType() == "tr_Coma":
                self.position += 1
                token = self.observeToken(self.position)
                if token.getType() == "Contenido":
                    self.insideParenthesesNumbers()
                else:
                    self.addError(token.getLexeme(), token.getLine(), token.getColumn(), "Contenido", f'Se obtuvo token "{ token.getLexeme() }" no esperado.')
                    return
        return
    
    def advancePositions(self, line):
        while True:
            token = self.observeToken(self.position)
            if token.getLine() == line:
                self.position += 1
            else:
                break

    def advance(self):
        try:
            while True:
                token = self.observeToken(self.position)
                if token.getType() == "tr_MenorQue":
                    break
                else:
                    self.position += 1
        except IndexError:
            return
        except AttributeError:
            return