from typing import runtime_checkable
from flask import Flask, render_template
import modulo1 
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import modulo2

res2 = modulo2.iniciar()


res = modulo1.iniciar()
import conversacion   #asi se llama el archivo python
res1 = conversacion.archivo()
# objeto apara crear rutas
app = Flask(__name__)
# Carpeta de subida
app.config['UPLOAD_FOLDER'] = "static/archivos"

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

#pagina cargar archivo
@app.route('/cargar')
def cargar():
    return render_template('cargar.html')
    
@app.route('/bloqueaMsj')
def bloquea():
    return render_template('bloqueaMsj.html', resModulo2=res)

@app.route('/mensajes-agresivos')
def filtro_msj_agr():
    return render_template('filtro-msj-agr.html',resModulo1=res)

@app.route('/simulacion-chat')
def simulacion_chat():
    return render_template('mensajes_agresivos.html',resarchivo=res1)

    #return emoji_pattern.sub(r'', mensajes)



@app.route("/uploader", methods=['POST'])
def uploader():
    if request.method == "POST":
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio "Archivos"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        msg='se subio el archivo correctamente'
        return render_template ('cargar.html',msg=msg)

# ctrl+shift+r para recargar sin cache
if __name__ == '__main__':
   app.run(debug=True)