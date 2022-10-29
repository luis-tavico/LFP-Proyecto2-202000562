class GenerateReportTokens:
  
  def __init__(self, tokens):
    self.tokens = tokens
    self.report = ""
    self.crearArchivo()

  def crearArchivo(self):
    self.report += """<!DOCTYPE html>
    <html lang="es">
      <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Tokens_202000562</title>
        <link rel="stylesheet" href="styleTables.css" />
      </head>
      <body>
        <div class="container">
          <h2>TABLA DE TOKENS</h2>
          <table>
            <thead>
              <tr>
                <th>No.</th>
                <th>Lexema/Token</th>
                <th>Tipo</th>
                <th>Columna</th>
                <th>Linea</th>
              </tr>
            </thead>
            <tbody>\n"""
    for token in self.tokens:
        self.report += '              <tr>\n'
        self.report += '                <td>'+ str(token.getNumber()) +'</td>\n'
        self.report += '                <td>'+ token.getLexeme() +'</td>\n'
        self.report += '                <td>'+ token.getType() +'</td>\n'
        self.report += '                <td>'+ str(token.getColumn()) +'</td>\n'
        self.report += '                <td>'+ str(token.getLine()) +'</td>\n'
        self.report += '              </tr>\n'
    self.report += """            </tbody>
          </table>
        </div>
      </body>
    </html>"""

    archivo = open("Tokens_202000562.html", "w")
    archivo.write(self.report)
    archivo.close()