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

import pprint


def iniciar():
    train = pd.read_csv('static/files/train_aggressiveness.csv', encoding = 'utf-8')
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

    # print(df.head(15))

    # Opening JSON file
    f = open('static/files/conversation001.json', encoding="utf8")

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    mensajes=[]
    for i in data['messages']:
    # print(i['text'])
        menU = (i['from'])
        tex = (i['text'])
        men=(menU+tex)
        mensajes.append(men)
        #mensajes.append(i['text'])
    # Closing file
    f.close()

    mensajes_nolist=[]
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
            continue

    determinantes = []
    mensajes_Noagresivos = []
    for elem in mensajes_nolist:
        if type(elem)==str:
            # print(elem)
            determinante = model.predict(vect.transform([elem]))
            if determinante == 0:
                mensajes_Noagresivos.append(elem)
            determinantes.append(determinante)

    contador = 0
    for elem in determinantes:
        if elem == 0:
            tipo = 'NO AGRESIVO'
            print('El mensaje ',contador,' es ',tipo)
        else:
            tipo = 'AGRESIVO'
            print('El mensaje ',contador,' es ',tipo)
        contador = contador + 1

    with open('text_classifier', 'wb') as picklefile:
        pickle.dump(model,picklefile)

    return mensajes_Noagresivos

    

    

