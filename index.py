import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


# objeto apara crear rutas
app = Flask(__name__)
# Carpeta de subida
app.config['UPLOAD_FOLDER'] = "static/archivo"

#pagina cargar archivo
@app.route('/cargar')
def cargar():
    return render_template('cargar.html')

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