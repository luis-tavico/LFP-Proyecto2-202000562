class StyleTable:

    def __init__(self):
        self.crearArchivo()

    def crearArchivo(self):
        contenido = """body {
    margin: 0;
    background: linear-gradient(45deg, #49a09d, #5f2c82);
    min-height: 100vh;
    font-family: sans-serif;
    font-weight: 100;
}

.container {
    padding-top: 10%;
    padding-bottom: 10%;
}

h2 {
    text-align: center;
    color: #fff;
    margin-top: 0%;
}

table {
    width: 80%;
    border-collapse: collapse;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    margin: 0 auto;
}

th, td {
    padding: 15px;
    text-align: center;
    background-color: rgba(255, 255, 255, 0.2);
    color: #fff;
}

thead th {
    background-color: #55608f;
}

tbody tr:hover {
    background-color: rgba(255, 255, 255, 0.3);
}

tbody td {
    position: relative;
}"""

        archivo = open("styleTables.css", "w")
        archivo.write(contenido)
        archivo.close()