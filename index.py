from flask import Flask, render_template, request, url_for, make_response
from werkzeug.utils import secure_filename
from typing import *
import modulo2
import pdfkit
import os

# lista que almacena lo que retorna modulo2
res = []

# objeto apara crear rutas
app = Flask(__name__)

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
    return render_template('simulacion-chat.html',datos=res)

#elige que filtrar
@app.route('/elegir-filtros',methods=['POST','GET'])
def elegir_filtros():
    return render_template('elegir-filtros-rs.html')

#elige que bloquear
@app.route('/elegir-bloqueos',methods=['POST','GET'])
def elegir_bloqueos():
    return render_template('elegir-bloqueos-rs.html')

# resultados de la eleccion de filtros
@app.route('/resultado-filtros', methods=['POST','GET'])
def resultado_filtros():
    if request.method=='POST':
        opciones = request.form.getlist('filtrosm')
    return render_template('resultado_filtros.html',datos=res, op=opciones)

# resultados de lo que bloqueo
@app.route('/resultado-filtros-bloqueados', methods=['POST','GET'])
def resultado_filtros_bloqueados():
    if request.method=='POST':
        opciones = request.form.getlist('bloqueos')
    return render_template('resultado_filtros_bloqueados.html',datos=res, op=opciones)

# muestra mensajes agresivos
@app.route('/mensajes-agresivos')
def filtro_msj_agr():
    return render_template('filtro-msj-agr.html',datos=res)

# bloquea mensajes agresivos
@app.route('/bloqueaMsj')
def bloquea():
    return render_template('bloqueaMsj.html', datos=res)

# reporte de agresion gv
@app.route('/reporte-gv')
def make_reportGV():
    return render_template('reporte-gv.html',datos=res)

@app.route('/reporte-dw')
def make_reportDW():
    return render_template('reporte-dw.html',datos=res)

# descargar el PDF
@app.route('/descargar')
def dw_reporte():
    options = {"enable-local-file-access": None}
    path_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    f=open("./templates/reporte-dw.html","r")
    pdf = pdfkit.from_file(f,'out.pdf', configuration=config, options=options)
    return render_template('reporte-dw.html')

# pagina de contacto
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')
    
# Carpeta de subida
app.config['UPLOAD_FOLDER'] = "static/archivos"

# cargar archivo a server
@app.route("/uploader", methods=['POST','GET'])
def uploader():
    if request.method == "POST":
        tipo = request.form['tipo']
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio "Archivos"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],'archivo.json'))
        msg='Archivo cargado con exito'
        res.append(modulo2.iniciar())
        for elem in res:
            print(elem)
        if tipo == 'rs':
            return render_template ('cargar-rs.html',msg=msg)
        elif tipo == 'gv':
            return render_template('cargar-gv.html',msg=msg)
        elif tipo == 'ac':
            return render_template('cargar-ac.html',msg=msg)

# ctrl+shift+r para recargar sin cache
if __name__ == '__main__':
   app.run(debug=True)