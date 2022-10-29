class ModelHTMLandCSS:

    def __init__(self, type='""', id='""', position=None, top=None, left=None, width=None, height=None, color=None, size=None,
                 background=None, backgroun_color=None, font_size=None, text_align=None, group="", checked="", text=""):
        self.type = type
        self.id = id
        self.position = position
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.color = color
        self.size = size
        self.background = background
        self.backgroun_color = backgroun_color
        self.font_size = font_size
        self.text_align = text_align
        self.group = group
        self.checked = checked
        self.text = text
        self.attributes = []

    def getType(self):
        return self.type

    def getId(self):
        return self.id

    def getPosition(self):
        return self.position

    def getTop(self):
        return self.top

    def getLeft(self):
        return self.left

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getColor(self):
        return self.color

    def getSize(self):
        return self.size

    def getBackground(self):
        return self.background

    def getBackgroun_color(self):
        return self.backgroun_color

    def getGroup(self):
        return self.group

    def getChecked(self):
        return self.checked

    def getFont_size(self):
        return self.font_size

    def getTextAlign(self):
        return self.text_align
    
    def getText(self):
        return self.text

    def setType(self, type):
        self.type = type

    def setId(self, id):
        self.id = id

    def setPosition(self, position):
        self.position = position

    def setTop(self, top):
        self.top = top

    def setLeft(self, left):
        self.left = left

    def setWidth(self, width):
        self.width = width

    def setHeight(self, height):
        self.height = height

    def setColor(self, color):
        self.color = color

    def setSize(self, size):
        self.size = size

    def setBackground(self, background):
        self.background = background

    def setBackgroun_color(self, backgroun_color):
        self.backgroun_color = backgroun_color

    def setChecked(self, checked):
        if checked == "true":
            self.checked = "checked"
 
    def setFont_size(self, font_size):
        self.font_size = font_size

    def setText(self, text):
        self.text = text
    
    def setGroup(self, group):
        self.group = group

    def setText_align(self, text_align):
        self.text_align = text_align
    
    def getAttribute(self):
        strng = ""
        for attribute in self.attributes:
            strng += attribute.getHTML()
        return strng

    def setAttribute(self, attribute):
        self.attributes.append(attribute)

    def getHTML(self):
        strg = ""
        if self.type == "label":
            strg = '<label id="'+self.getId()+'">'+self.getText()+'</label>\n'
        elif self.type == "submit":
            strg = '<input type="submit" id="'+self.getId()+'" value="'+self.getText()+'">\n'
        elif self.type == "checkbox":
            strg = '<input type="checkbox" id="'+self.getId()+'" '+self.getChecked()+'>'+self.getText()
        elif self.type == "radio":
            strg = '<input type="radio" id="'+self.getId()+'" name="'+self.getGroup()+'" '+self.getChecked()+'>'+self.getText()
        elif self.type == "text":
            strg = '<input type="text" id="'+self.getId()+'" value="'+self.getText()+'">\n'
        elif self.type == "textarea":
            strg = '<textarea id="'+self.getId()+'">'+self.getText()+'</textarea>\n'
        elif self.type == "password":
            strg = '<input type="password" id="'+self.getId()+'" value="'+self.getText()+'">\n'
        elif self.type == "div":
            strg = '<div id="'+self.getId()+'">\n'
            strg += self.getAttribute()
            strg += '</div>\n'
        return strg

    def getCSS(self):
        strng = ""
        string = "#"+self.getId()+"{\n"
        if self.getPosition() != None: strng += "   position: "+str(self.getPosition())+";\n"
        if self.getTop() != None: strng += "   top: "+str(self.getTop())+";\n"
        if self.getLeft() != None: strng += "   left: "+str(self.getLeft())+";\n"
        if self.getWidth() != None: strng += "   width: "+str(self.getWidth())+";\n"
        if self.getHeight() != None: strng += "   height: "+str(self.getHeight())+";\n"
        if self.getColor() != None: strng += "   color: "+str(self.getColor())+";\n"
        if self.getSize() != None: strng += "   size: "+str(self.getSize())+";\n"
        if self.getBackground() != None: strng += "   background: "+str(self.getBackground())+";\n"
        if self.getBackgroun_color() != None: strng += "   background-color: "+str(self.getBackgroun_color())+";\n"
        if self.getFont_size() != None: strng += "   font-size: "+str(self.getFont_size())+";\n"
        if self.getTextAlign() != None: strng += "   text-align: "+str(self.getTextAlign())+";\n"
        if strng == "":
            return ""
        string += strng+"}\n"
        return(string)