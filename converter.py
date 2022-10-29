from modelHtmlandCSS import ModelHTMLandCSS

class Converter:

    def __init__(self):
        self.scanner = ""
        self.listTag = []
        self.listTagforHtml = []
        self.alignment = {"Izquierdo":"left", "Centro":"center", "Derecho":"right"}

    def readContent(self, content):
        instructionCnts = False
        instructionPpts = False
        instructionPmnt = False
        commentary = False
        for line in content.split('\n'):
            for lexeme in line:

                if commentary:
                    self.scanner += lexeme
                else:      
                    if lexeme == " " or lexeme == "\t" or lexeme == ";":
                        pass
                    else:   
                        self.scanner += lexeme

            if self.scanner == "":
                continue

            #check if content is comment
            if self.scanner[0] == "/" and self.scanner[1] == "/":
                self.scanner = ""
                continue
            elif "/*" in self.scanner and "*/" in self.scanner:
                self.scanner = ""
                continue
            elif "/*" in self.scanner:
                commentary = not(commentary)
            elif "*/" in self.scanner:
                commentary = not(commentary)

            #If content not is comment
            if commentary == False:
                if "Controles" in self.scanner:
                    instructionCnts = not(instructionCnts)
                elif "propiedades" in self.scanner:
                    instructionPpts = not(instructionPpts)
                elif "Colocacion" in self.scanner:
                    instructionPmnt = not(instructionPmnt)

                if instructionCnts: 
                    self.instructionControls()
                elif instructionPpts: 
                    self.instructionProperties()
                elif instructionPmnt:
                    self.instructionPlacement()

            self.scanner = ""

        html = '<!DOCTYPE html>'
        html += '<html lang="en">\n'
        html += '<head>\n'
        html += '    <meta charset="UTF-8">\n'
        html += '    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n'
        html += '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        html += '    <link rel="stylesheet" href="style.css">\n'
        html += '    <title>PaginaFinal</title>\n'
        html += '</head>\n'
        html += '<body>\n'
        for tag in self.listTagforHtml:
            html += tag.getHTML()
        html += '</body>\n'
        html += '</html>'
        fileHtml = open("./paginaWeb.html", "w")
        fileHtml.write(html)
        fileHtml.close()


        css = ""
        for tag in self.listTag:
            css += tag.getCSS()
        fileCss = open("./style.css", "w")
        fileCss.write(css)
        fileCss.close()

    def instructionControls(self): 
        newTag = None
        if "Etiqueta" in self.scanner:
            id = self.scanner.replace("Etiqueta", "", 1)
            newTag = ModelHTMLandCSS(type="label", id=id, font_size="12px", height="25px", width="100px")
        elif "RadioBoton" in self.scanner:
            id = self.scanner.replace("RadioBoton", "", 1)
            newTag = ModelHTMLandCSS(type="radio", id=id)
        elif "Boton" in self.scanner:
            id = self.scanner.replace("Boton", "", 1)
            newTag = ModelHTMLandCSS(type="submit", id=id, text_align="left", font_size="12px", height="25px", width="100px")
        elif "Check" in self.scanner:
            id = self.scanner.replace("Check", "", 1)
            newTag = ModelHTMLandCSS(type="checkbox", id=id)
        elif "AreaTexto" in self.scanner:
            id = self.scanner.replace("AreaTexto", "", 1)
            newTag = ModelHTMLandCSS(type="textarea", id=id, height="150px", width="150px")
        elif "Texto" in self.scanner:
            id = self.scanner.replace("Texto", "", 1)
            newTag = ModelHTMLandCSS(type="text", id=id, text_align="left", height="25px", width="100px")
        elif "Clave" in self.scanner:
            id = self.scanner.replace("Clave", "", 1)
            newTag = ModelHTMLandCSS(type="password", id=id, text_align="left", height="25px", width="100px")
        elif "Contenedor" in self.scanner:
            id = self.scanner.replace("Contenedor", "", 1)
            newTag = ModelHTMLandCSS(type="div", id=id, font_size="12px")
        if newTag != None:
            self.listTagforHtml.append(newTag)
            self.listTag.append(newTag)

    def instructionProperties(self): 
        tag = self.scanner.split('.')
        for tg in self.listTag:
            if tg.getId() == tag[0]:
                if "setColorLetra" in tag[1]:
                    color = tag[1][tag[1].index("(")+1:tag[1].index(")")]
                    tg.setColor("rgb("+color+")")
                elif "setTexto" in self.scanner:
                    text = tag[1][tag[1].index("(")+1:tag[1].index(")")]
                    text = text.replace('"', '')
                    tg.setText(text)
                elif "setAlineacion" in self.scanner:
                    alignment = tag[1][tag[1].index("(")+1:tag[1].index(")")]
                    alignment = self.alignment[alignment]
                    tg.setText_align(alignment)
                elif "setColorFondo" in self.scanner:
                    bcolor = tag[1][tag[1].index("(")+1:tag[1].index(")")]
                    tg.setBackgroun_color("rgb("+bcolor+")")    
                elif "setMarcada" in self.scanner:
                    value = tag[1][tag[1].index("(")+1:tag[1].index(")")]
                    tg.setChecked(value)
                elif "setGrupo" in self.scanner:
                    group = tag[1][tag[1].index("(")+1:tag[1].index(")")]
                    tg.setGroup(group)
                elif "setAlto" in self.scanner:
                    height = tag[1][tag[1].index("(")+1:tag[1].index(")")]+"px"
                    tg.setHeight(height) 
                elif "setAncho" in self.scanner:
                    width = tag[1][tag[1].index("(")+1:tag[1].index(")")]+"px"
                    tg.setWidth(width)   


    def instructionPlacement(self): 
        tag = self.scanner.split('.')
        for tg in self.listTag:
            if tg.getId() == tag[0]:
                if "setPosicion" in self.scanner:
                    position = tag[1][tag[1].index("(")+1:tag[1].index(")")]
                    position = position.split(",")
                    tg.setPosition("absolute")
                    tg.setLeft(position[0]+"px")   
                    tg.setTop(position[1]+"px")   
                elif "add" in self.scanner:
                    idDiv = tag[0]
                    idAttr = tag[1][tag[1].index("(")+1:tag[1].index(")")]
                    attr = None
                    for t in self.listTag:
                        if t.getId() == idAttr:
                            attr = t
                            break
                    for t in self.listTag:
                        if t.getId() == idDiv:
                            if attr != None:
                                t.setAttribute(attr)
                                break
                    i = 0
                    for t in self.listTagforHtml:
                        if t.getId() == idAttr:
                            self.listTagforHtml.pop(i)
                            break
                        i += 1