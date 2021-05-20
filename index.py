from typing import runtime_checkable
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import modulo1 
import modulo2
import conversacion  

res = modulo1.iniciar()
res1 = conversacion.archivo()
res2 = modulo2.iniciar()

# objeto apara crear rutas
app = Flask(__name__)

# Carpeta de subida
app.config['UPLOAD_FOLDER'] = "static/archivos"

# / es pagina principal
@app.route('/')
def index():
    return render_template('index.html')

# eleccion de usuario
@app.route('/eleccion')
def eleccion():
    return render_template('eleccion_usuarios.html')

# pagina cargar archivo de redes sociales
@app.route('/cargar-rs')
def cargar_rs():
    return render_template('cargar-rs.html')

# pagina cargar archivo de grupo vulnerable
@app.route('/cargar-gv')
def cargar_gv():
    return render_template('cargar-gv.html')

# pagina cargar archivo de academico
@app.route('/cargar-ac')
def cargar_ac():
    return render_template('cargar-ac.html')

# simulacion de chat
@app.route('/simulacion-chat')
def simulacion_chat():
    return render_template('simulacion-chat.html',resarchivo=res)

# muestra mensajes agresivos
@app.route('/mensajes-agresivos')
def filtro_msj_agr():
    return render_template('filtro-msj-agr.html',resModulo1=res)

# bloquea mensajes agresivos
@app.route('/bloqueaMsj')
def bloquea():
    return render_template('bloqueaMsj.html', resModulo2=res)

# pagina de contacto
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')
    
# cargar archivo a server
@app.route("/uploader", methods=['POST'])
def uploader():
    if request.method == "POST":
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio "Archivos"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        msg='se subio el archivo correctamente'
        return render_template ('cargar-rs.html',msg=msg)

# ctrl+shift+r para recargar sin cache
if __name__ == '__main__':
   app.run(debug=True)