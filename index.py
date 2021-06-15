from flask import Flask, render_template, request, url_for, make_response
from werkzeug.utils import secure_filename
from typing import *
import modulo2
import pdfkit
import os

# lista que almacena lo que retorna modulo2
res = []
tipo=""
opciones=""
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
        for elem in res:    
            datos = modulo2.predecir_agresividad(elem)
        ua = modulo2.obtener_usuarios_agresivos(datos)
        print("LONDATOS:",len(datos))
    return render_template('resultado_filtros.html',datos=datos, op=opciones, ua=ua)

# resultados de lo que bloqueo
@app.route('/resultado-filtros-bloqueados', methods=['POST','GET'])
def resultado_filtros_bloqueados():
    if request.method=='POST':
        global opciones
        opciones = request.form.getlist('bloqueos')
        for elem in res:    
            datos = modulo2.predecir_agresividad(elem)
        ua = modulo2.obtener_usuarios_agresivos(datos)
        users = modulo2.creacion_objetos(ua)
        u_blocked = modulo2.bloquear_usuarios(users,opciones)
    return render_template('resultado_filtros_bloqueados.html',datos=u_blocked, op=opciones)

# muestra mensajes agresivos
@app.route('/mensajes-agresivos')
def filtro_msj_agr():
    return render_template('filtro-msj-agr.html',datos=res)

# bloquea mensajes agresivos
@app.route('/bloqueaMsj')
def bloquea():
    for elem in res:    
        datos = modulo2.predecir_agresividad(elem)
    ua = modulo2.obtener_usuarios_agresivos(datos)
    users = modulo2.creacion_objetos(ua)
    u_blocked=[]
    u_blocked.append(modulo2.bloquear_usuarios(users,opciones))
    return render_template('bloqueaMsj.html', datos=res,ub=u_blocked,tipo=tipo, opciones=opciones)

# reporte de agresion gv
@app.route('/reporte-gv')
def make_reportGV():
    for elem in res:    
        datos = modulo2.predecir_agresividad(elem)
    ua = modulo2.obtener_usuarios_agresivos(datos)
    users = modulo2.creacion_objetos(ua)
    return render_template('reporte-gv.html',datos=users,mensajes=datos)

@app.route('/reporte-dw')
def make_reportDW():
    for elem in res:    
        datos = modulo2.predecir_agresividad(elem)
    ua = modulo2.obtener_usuarios_agresivos(datos)
    users = modulo2.creacion_objetos(ua)
    return render_template('reporte-dw.html',datos=users,mensajes=datos)

# descargar el PDF
@app.route('/descargar')
def dw_reporte():
    options = {"enable-local-file-access": None}
    path_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #f=open("./templates/reporte-dw.html","r")
    #pdf = pdfkit.from_file(f,'out.pdf', configuration=config, options=options)
    #return render_template('reporte-dw.html')
    for elem in res:    
        datos = modulo2.predecir_agresividad(elem)
    ua = modulo2.obtener_usuarios_agresivos(datos)
    users = modulo2.creacion_objetos(ua)
    html = render_template(
        "reporte-gv.html",
        datos=users,mensajes=datos)
    pdf = pdfkit.from_string(html, False,configuration=config, options=options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=reporte-evidencia.pdf"
    return response

# pagina de contacto
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/acerca')
def acerca():
    return render_template('acerca.html')

# Carpeta de subida
app.config['UPLOAD_FOLDER'] = "static/archivos"

# cargar archivo a server
@app.route("/cargar_archivo", methods=['POST','GET'])
def cargar_archivo():
    if request.method == "POST":
        global tipo
        tipo = request.form['tipo']
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio "Archivos"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],'archivo.json'))
        msg='Archivo cargado con exito'
        res.append(modulo2.leer_archivo())
        nombre_archivo, extension = os.path.splitext("archivo.json")
        if extension=="json":
            for elem in res:
                print(elem)
            if tipo == 'rs':
                return render_template ('cargar-rs.html',msg=msg)
            elif tipo == 'gv':
                return render_template('cargar-gv.html',msg=msg)
            elif tipo == 'ac':
                return render_template('cargar-ac.html',msg=msg)
        else:
            msg="Error. Solo se aceptan archivos en formato JSON"
            return render_template ('cargar-rs.html',msg=msg)

@app.route('/reporte-ac')
def reporte_ac():
    for elem in res:    
        datos = modulo2.predecir_agresividad(elem)
    ua = modulo2.obtener_usuarios_agresivos(datos)
    users = modulo2.creacion_objetos(ua)
    ub = modulo2.bloquear_usuarios(users)
    ac = modulo2.reporte_academico(ub)

    nueva = 0 
    nueva2 = 0
    nueva3 = 0
    
    nueva = len(datos[0])
    nueva2 = len(datos[1])
    nueva3=nueva2+nueva

    return render_template('reporte-ac.html',datos=ac,elem=nueva,elem1=nueva2,elem2=nueva3)

# ctrl+shift+r para recargar sin cache
if __name__ == '__main__':
   app.run(debug=True)