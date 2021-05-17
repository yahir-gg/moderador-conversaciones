from typing import runtime_checkable
from flask import Flask, render_template
import conversacion   #asi se llama el archivo python
res = conversacion.archivo()
# objeto apara crear rutas
app = Flask(__name__)

# / es pagina principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')



@app.route('/mensajes_agresivos')

def chat():
        return render_template('mensajes_agresivos.html',resarchivo=res)

    #return emoji_pattern.sub(r'', mensajes)




# ctrl+shift+r para recargar sin cache
if __name__ == '__main__':
   app.run(debug=True)