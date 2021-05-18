import json


def archivo():
    ruta = ('C:/Users/tania/OneDrive/Documentos/tematico_4/moderador/static/archivos/result.json')
    with open(ruta) as contenido:
        datos = json.load(contenido)#carga los archivos json
        mensajes = []# es una lista 
      
    for i in datos['messages']: #recorre la lista con la varible datos y la va almacenando en i
             mensajes.append(i) #append es para colocar los elementos en la lista 
    for i in mensajes:#vuelve a recorrer la lista para imprimir los valores
                print(i['from'])
               
                print(i['date'])
                print(i['text'])
                print("")
    
    return mensajes
    
