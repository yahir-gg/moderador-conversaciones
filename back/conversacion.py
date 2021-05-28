"""import json


def archivo():
    ruta = ('C:/Users/kenyg/developer/proyecto-lt4/moderador/static/archivos/conversation001.json')
    with open(ruta, encoding="utf-8") as contenido:
        datos = json.load(contenido)#carga los archivos json
        mensajes = []# es una lista 
      
    for i in datos['messages']: #recorre la lista con la varible datos y la va almacenando en i
        mensajes.append(i) #append es para colocar los elementos en la lista 
    # vuelve a recorrer la lista para imprimir los valores
    for i in mensajes:
        if i['type'] == 'message':
            print(i['from'])
            print(i['date'])
            print(i['text'])
            print("")
        
    return mensajes"""
    
