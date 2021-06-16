from flask import render_template, make_response
from collections import Counter
from fpdf import Template
import joblib
import pdfkit
import json
import os
import re

model=joblib.load('model.pkl')
vect=joblib.load('vectorizer.pkl')

def leer_archivo():

    mensajes=[]
    conv_users = []

    try:
        f = open('./static/archivos/archivo.json', encoding="utf8")
        data = json.load(f)

        for i in data['messages']:
            mensajes.append(i)

        cont = 0
        
        for i in mensajes:
            if i['text'] == "":
                mensajes.pop(cont)
            cont += 1
        
        for elem in mensajes:
            if elem['type'] == 'message':
                if elem['from'] not in conv_users:
                    conv_users.append(elem['from'])

        f.close()
    except:
        print('Error. No se pudo abrir el archivo.')
    return mensajes,conv_users
    
def predecir_agresividad(lista):
    mensajes = lista[0]
    determinantes = []
    mensajes_agresivos = []
    mensajes_no_agresivos = []


    for elem in mensajes:
        aux = elem['text']
        determinante = model.predict(vect.transform([aux]))
        if determinante == 1:
            mensajes_agresivos.append(elem)
        elif determinante == 0:
            mensajes_no_agresivos.append(elem)
        determinantes.append(determinante)

    return mensajes_agresivos, mensajes_no_agresivos

def obtener_usuarios_agresivos(lista):    
    usuarios_agresivos=[]
    mensajes_agresivos = lista[0]
    # recorremos la lista de mensajes agresivos
    for e in mensajes_agresivos:
        # verificamos que no se repitan los nombres
        if e['from'] not in usuarios_agresivos:
        # se agrega el user a la lista
            usuarios_agresivos.append(e['from'])

    return usuarios_agresivos
    
def creacion_objetos(lista):
    class Objeto:
        nombre = ""
        id = ""
        #cantidad (de mensajes agresivos)
        cantidad = 0
        totalmsj = 0
        msj_agr = []

    usuarios_agresivos = lista
    users = []
    # recorremos la lista de user agresivos
    data = leer_archivo()
    predicciones = predecir_agresividad(data)
    mensajes_agresivos = predicciones[0]
    conv_users=data[1]
    for e in usuarios_agresivos:
        # se crea objeto
        o = Objeto()
        # asignacion de nombre
        o.nombre = str(e)
        # cantidad por default se pone en 0
        # el objeto se añade a la lista users
        users.append(o)
        for f in mensajes_agresivos:
            if f['from'] == e:
                o.id = f['from_id']
                #o.msj_agr=f['text']
                break
        print('Objeto ',e, 'creado')
    
    cont = 0
    # recorremos la lista de msj agresivos
    
                             



    for d in mensajes_agresivos:
        # recorremos la lista de objetos
        for h in users:
        # verificamos si el usuario agresivo tiene un objeto creado
            if d['from'] == h.nombre:
                # se aumenta en uno la cantidad de msj agr
                h.cantidad+=1
    
    # recorremos la lista de objetos
    
    mensajes = data[0]
    for p in mensajes:
        for q in users:
            if p['from'] == q.nombre:
                q.totalmsj+=1
    
    return users
    """listadic=[]
    for persona in users:  
        diccionario = {'nombre' : persona.nombre, 'id' : persona.id, 'nma': persona.cantidad, 'msjt': persona.totalmsj }
        listadic.append(diccionario)"""
    
def bloquear_usuarios(users, opciones):
    blockUsers = []
    no_bk_users=[]
    block_msj=[]

    userSlice  = slice(3)
    for o in users:
        if o.cantidad >= 2:
            blockUsers.append(o.nombre)
    data = leer_archivo()
    pred = predecir_agresividad(data)
    all_user = data[1]
    for u in all_user:
        if u not in blockUsers:
            no_bk_users.append(u)
            
    msj_av=[]
    msj_bk=[]
    data = leer_archivo()
    mensajes = data[0]
    for e in blockUsers:
        for i in mensajes:
            if i['from'] not in blockUsers:
                msj_av.append(i['text'])
            else:
                msj_bk.append(i['text'])
    
    if len(opciones)==2:
        return blockUsers,pred[0],pred[1], no_bk_users, pred[1]
    else:
        for op in opciones:
            if op == "2":
                return blockUsers,msj_bk,msj_av, no_bk_users, mensajes
            elif op=="1":
                return blockUsers,pred[0],pred[1], all_user, pred[1]
            

                
            
   


    #print(bloqueaUsers)

    #resultado[0][3]
def reporte_academico(lista,opciones):
    blockUsers = lista
    msjAgrUs = []
    data = leer_archivo()
    determinantes = predecir_agresividad(data)
    mensajes_agresivos = determinantes[0]
    mensajes_no_agresivos = determinantes[1]

    for w in blockUsers:
        for q in mensajes_agresivos:
            if q['from']==w:
                msjAgrUs.append(q['text'])
    

    #print(msjAgrUs)
    date = []
    for e in mensajes_agresivos:
        if e['date'] not in date:
            date.append(e['date'])
            x= slice(0,8,7)
            
    #En esta parte se casa la longitud de las lista de mensajes no agresivos y si agresivos
    total=[]
    total.append(len(mensajes_no_agresivos))

    total2=[]
    total2.append(len(mensajes_agresivos))

    #mensajes mas utilizados
    listaRep = []
    for m in mensajes_agresivos:
        texto = re.findall('\w+',m['text'])
        for l in texto:
            if len(l) > 5:
                listaRep.append(l)

    contador = Counter(listaRep)
    mas_rep = contador.most_common(2)
    return date[x],total,total2, mas_rep