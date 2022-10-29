import os
from tkinter import filedialog, messagebox, ttk
from tkinter import *
from syntacticAnalyzer import SyntacticAnalyzer
from lexicalAnalyzer import LexicalAnalyzer
from reportTokens import GenerateReportTokens
from styleTables import StyleTable
from converter import Converter

class Interface:
    
    def __init__(self, window):
        self.window = window
        windowWidth, windowHeight = 700, 400
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        positionX = int(screenWidth/2 - windowWidth/2)
        positionY = int(screenHeight/2 - windowHeight/2)
        self.window.geometry(f'{windowWidth}x{windowHeight}+{positionX}+{positionY}')
        self.window.minsize(700, 400)
        self.window.title("AnalizadorApp")
        self.window.resizable(True, True)
        #self.window.protocol("WM_DELETE_WINDOW", self.salir)
        self.window.bind_all("<Control-n>", self.new)
        self.window.bind_all("<Control-o>", self.open)
        self.window.bind_all("<Control-s>", self.save)
        self.window.bind_all("<Control-Shift-S>", self.saveAs)
        self.path = ""
        self.contentArchive = ""
        self.contentTextArea = ""
        self.listError = []
        self.initComponents()

    def initComponents(self):
        self.addPanel()
        self.addMenu()
        self.addTextField()
        self.addLabel()
        self.addTable()
        self.textInput.bind("<ButtonRelease-1>", self.position)
        self.textInput.bind("<KeyRelease>", self.position)

    def addPanel(self):
        self.panel = Frame(self.window)
        self.panel.pack(fill="both", expand="true")

    def addMenu(self):
        self.menu = Menu(self.window)
        self.fileMenu = Menu(self.menu, tearoff=0)
        self.fileMenu.add_command(label="Nuevo", accelerator="Ctrl+N", command=self.new)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Abrir", accelerator="Ctrl+O", command=self.open)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Guardar", accelerator="Ctrl+S", command=self.save)
        self.fileMenu.add_command(label="Guardar como", accelerator="Ctrl+Shift+S", command=self.saveAs)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Salir", command=self.exit)
        self.menu.add_cascade(menu=self.fileMenu, label="Archivo")
        self.menu.add_command(label="Analizar", command=self.analyze)
        self.menu.add_command(label="Tokens", command=self.tokens)
        self.window.config(menu=self.menu)

    def addTextField(self):
        self.textInput = Text(self.panel, font=("Segoe UI", 11), bd=0, padx=10, pady=10)
        self.textInput.place(relx=0.02, rely=0, relheight=0.63, relwidth=0.96)
        #scroll
        scrollbar = ttk.Scrollbar(self.panel, orient=VERTICAL, command=self.textInput.yview)
        self.textInput.configure(yscroll=scrollbar.set)
        scrollbar.place(relx=0.98, rely=0, relheight=0.63, relwidth=0.02)
        self.textInput.focus_set()
        
    def addLabel(self):
        self.label = Label(self.panel, font=("Arial", 10), bd=0, text="Linea: 1    Columna: 1")
        self.label.place(rely=0.63, relheight=0.04, relwidth=1)

    def addTable(self):
        #columns
        columns = ('tipo_error', 'linea', 'columna', 'se_esperaba', 'descripcion')
        #Creating table
        self.table = ttk.Treeview(self.panel, columns=columns, show='headings')
        #define headings
        self.table.heading('tipo_error', text='Tipo de Error')
        self.table.heading('linea', text='Linea')
        self.table.heading('columna', text='Columna')
        self.table.heading('se_esperaba', text='Se esperaba')
        self.table.heading('descripcion', text='Descripcion')
        #columns
        self.table.column("tipo_error", width=100, anchor=CENTER)
        self.table.column("linea", width=75, anchor=CENTER)
        self.table.column("columna", width=75, anchor=CENTER)
        self.table.column("se_esperaba", width=210, anchor=CENTER)
        self.table.column("descripcion", width=210, anchor=CENTER)
        #position table
        self.table.place(relx=0.02, rely=0.67, relheight=0.32, relwidth=0.96)
        #scroll
        scrollbar = ttk.Scrollbar(self.panel, orient=VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        #scrollbar.grid(row=0, column=1, sticky='ns')
        scrollbar.place(relx=0.98, rely=0.67, relheight=0.32, relwidth=0.02)
        #insert values

    def position(self, e):
        line, column = self.textInput.index("insert").split('.')
        position = 'Linea: '+line+'    Columna: '+str(int(column)+1)
        self.label.configure(text=position)

    def new(self, event=None):
        self.contentTextArea = self.textInput.get(1.0, "end-1c")
        if self.contentTextArea != self.contentArchive:
            reply = messagebox.askyesnocancel("Pregunta", "¿Desea guardar los cambios?")
            if reply:
                r = self.save()
                if r:
                    self.textInput.delete(1.0, "end")
                    self.contentTextArea = self.textInput.get(1.0, "end-1c")
                    self.contentArchive = self.contentTextArea
                    self.path = ""
                    self.clearTable()
                    return True
            elif reply == False:
                self.textInput.delete(1.0, "end")
                self.contentTextArea = self.textInput.get(1.0, "end-1c")
                self.contentArchive = self.contentTextArea
                self.path = ""
                self.clearTable()
                return True
            elif reply == None:
                return False
        else:
            self.textInput.delete(1.0, "end")
            self.contentTextArea = self.textInput.get(1.0, "end-1c")
            self.contentArchive = self.contentTextArea
            self.path = ""
            self.clearTable()
            return True

    def open(self, event=None):
        r = self.new()
        if r:
            self.path = filedialog.askopenfilename(title="Abrir", filetypes=(("Archivo GPW", "*.gpw"), ("Todos los Archivos", "*.*")))
            if self.path != "":
                path, extension = os.path.splitext(self.path)
                if extension.lower() == ".gpw":
                    self.textInput.delete(1.0, "end")
                    file = open(self.path, 'r')
                    self.contentArchive = file.readlines()
                    file.close()
                    self.contentArchive = "".join(self.contentArchive)
                    self.textInput.insert('insert', self.contentArchive)
                    self.contentTextArea = self.textInput.get(1.0, "end-1c")
                else: 
                    messagebox.showwarning("Advertencia", "¡La extension del archivo es incorrecta!\nUnica extension aceptada -> (.gpw)")

    def save(self, event=None):
        self.contentTextArea = self.textInput.get(1.0, "end-1c")
        if self.path != "":
            file = open(self.path, "w")
            file.write(self.contentTextArea)
            file.close()
            self.contentArchive = self.contentTextArea
            return True
        else:
            r = self.saveAs()
            return r

    def saveAs(self, event=None):
        self.contentTextArea = self.textInput.get(1.0, "end-1c")
        file = filedialog.asksaveasfile(title="Guardar como", mode="w", defaultextension=".gpw", filetypes=(("Archivo GPW", "*.gpw"),("Archivo TXT", "*.txt")))
        if file != None:
            self.path = file.name
            file = open(self.path, "w")
            file.write(self.contentTextArea)
            file.close()
            self.contentArchive = self.contentTextArea
            messagebox.showinfo("Informacion", "¡Archivo Guardado Exitosamente!")
            return True
        return False
    
    def exit(self):
        self.contentTextArea = self.textInput.get(1.0, "end-1c")
        if self.contentTextArea != self.contentArchive:
            reply = messagebox.askyesnocancel("Pregunta", "¿Desea guardar los cambios?")
            if reply:
                r = self.save()
                if r:
                    self.window.destroy()
            elif reply == False:
                self.window.destroy()
        else:
            self.window.destroy()

    def analyze(self):
        self.clearTable()
        content = self.textInput.get(1.0, "end-1c")
        if content != "":
            lexicalAnalyzer = LexicalAnalyzer()
            lexicalAnalyzer.analyzer(content)
            tokens = lexicalAnalyzer.tokens
            listErrorL = lexicalAnalyzer.errores
            self.addErrorToTable(listErrorL)
            GenerateReportTokens(tokens)
            StyleTable()
            syntacticAnalyzer = SyntacticAnalyzer(tokens)
            syntacticAnalyzer.analyzer()
            listErrorS = syntacticAnalyzer.errores
            self.addErrorToTable(listErrorS)
            if len(listErrorL) == 0 and len(listErrorS) == 0:
                converter = Converter()
                converter.readContent(content)
                os.system("paginaWeb.html")

    def addErrorToTable(self, listError):
        self.listError = listError
        if len(self.listError) > 0:
            for error in self.listError:
                self.table.insert('', END, values=(error.getType(), error.getLine(), error.getColumn(), error.getExpected(), error.getDescription()))
    
    def clearTable(self):
        self.listError = []
        self.table.delete(*self.table.get_children())

    def tokens(self):
        os.system("Tokens_202000562.html")