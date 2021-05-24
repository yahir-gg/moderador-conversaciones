import numpy as np
import pandas as pd
import re
import nltk
import json
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
nltk.download('stopwords')
nltk.download('wordnet')
def iniciar():
    

    train = pd.read_csv('./static/archivos/train_aggressiveness.csv', encoding = 'utf-8')
    df = train.copy()
    # df.head()

    ", ".join(stopwords.words('spanish'))
    stops = set(stopwords.words('spanish'))


    # Funcion que limpia el texto
    def process_text(message):
        # Elimina hyperlinks.
        message = re.sub(r'https?://\S+|www\.\S+', '', message)

        # Elimina html
        message = re.sub(r'<.*?>', '', message)
        # Elimina numeros
        message = re.sub(r'\d+', '', message)
        # Elimina menciones de usuarios
        message = re.sub(r'@\w+', '', message)
        # Elimina puntuacion
        message = re.sub(r'[^\w\s\d]', '', message)
        # Elimina espacios en blanco
        message = re.sub(r'\s+', ' ', message).strip()
        # Elimina stopwords
        message = " ".join([word for word in str(message).split() if word not in stops])

        return message.lower()

    df['newText'] = df['Text'].apply(lambda x: process_text(x))
    def token_lemma(message):
        tk = TweetTokenizer()
        lemma = WordNetLemmatizer()
        message = tk.tokenize(message)
        message = [lemma.lemmatize(word) for word in message]
        message = " ".join([word for word in message])
        return message

    message = df['newText']
    # print(message)

    df['lemmaText'] = df['newText'].apply(lambda x: token_lemma(x))
    y = df["Category"]

    df['lemmaText'].head()

    vect = CountVectorizer(stop_words = 'english')
    X_train_matrix = vect.fit_transform(df["lemmaText"])

    X_train, X_test, y_train, y_test = train_test_split(X_train_matrix, y, test_size= 0.3)
    model = MultinomialNB()
    model.fit(X_train, y_train)
    # print (model.score(X_train, y_train))
    # print (model.score(X_test, y_test))
    predicted_result = model.predict(X_test)
    print("\n")
    # print(classification_report(y_test,predicted_result))

    df['prediccion'] = model.predict(vect.transform(df["lemmaText"]))

    # print(df["prediccion"])

    df['Determinante'] = df['prediccion'].apply(lambda prediccion:'No agresivo' if prediccion ==0 else 'Agresivo')
    with open('text_classifier', 'wb') as picklefile:
        pickle.dump(model,picklefile)
    
    #with open('text_classifier', 'rb') as training_model:
    #    model = pickle.load(training_model)
    # print(df.head(15))

    # Opening JSON file
    mensajes=[]
    conv_users = []
    try:
        f = open('./static/archivos/archivo.json', encoding="utf8")
        
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data['messages']:
            # print(i['text'])
            mensajes.append(i)

        
            
        # print(len(mensajes))
        cont = 0
        # print(mensajes)
        
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
        print('errorXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    """mensajes_nolist=[]
    # print("imp\n", mensajes)
    for elem in mensajes:
        if type(elem) == str:
            # process_text(elem)
            mensajes_nolist.append(elem)
        elif type(elem) == list:
            for elem2 in elem:
                # process_text(elem2)
                mensajes_nolist.append(elem2)
        else:
            continue"""

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
    print('dt:',determinantes)
    contador = 0
    """for elem in determinantes:
        if elem == 0:
            tipo = 'NO AGRESIVO'
            print('El mensaje ',contador,' es ',tipo)
        else:
            tipo = 'AGRESIVO'
            print('El mensaje ',contador,' es ',tipo)
        contador = contador + 1"""

    class Objeto:
        nombre = ""
        cantidad = 0
        # msj_agr = []
    
    usuarios_agresivos=[]
    # recorremos la lista de mensajes agresivos
    for e in mensajes_agresivos:
        # verificamos que no se repitan los nombres
        if e['from'] not in usuarios_agresivos:
        # se agrega el user a la lista
            usuarios_agresivos.append(e['from'])

    print(usuarios_agresivos)
    users = []
    # recorremos la lista de user agresivos
    for e in usuarios_agresivos:
        # se crea objeto
        o = Objeto()
        # asignacion de nombre
        o.nombre = str(e)
        # cantidad por default se pone en 0
        # el objeto se añade a la lista users
        users.append(o)
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
        
    print('Users')
    # recorremos la lista de objetos
    for h in users:
        print('User: ',h.nombre,' Num.MsjAgr: ',h.cantidad)

    return mensajes_agresivos, conv_users, mensajes, mensajes_no_agresivos, users
