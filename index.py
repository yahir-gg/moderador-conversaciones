from typing import runtime_checkable
from flask import Flask, render_template
import modulo1 

res = modulo1.iniciar()
import conversacion   #asi se llama el archivo python
res1 = conversacion.archivo()
# objeto apara crear rutas
app = Flask(__name__)

# / es pagina principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eleccion')
def eleccion():
    return render_template('eleccion_usuarios.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')
  
@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/cargar')
def cargar():
    return render_template('cargar.html')

@app.route('/mensajes-agresivos')
def filtro_msj_agr():
    return render_template('filtro-msj-agr.html',resModulo1=res)

@app.route('/simulacion-chat')
def simulacion_chat():
    return render_template('mensajes_agresivos.html',resarchivo=res1)

    #return emoji_pattern.sub(r'', mensajes)




# ctrl+shift+r para recargar sin cache
if __name__ == '__main__':
   app.run(debug=True)