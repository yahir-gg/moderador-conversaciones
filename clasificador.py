import numpy as np 
import pandas as pd 
import re 
import nltk
from nltk.corpus import stopwords
 
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import joblib
 
nltk.download('stopwords')
nltk.download('wordnet')

train = pd.read_csv('static/archivos/train_aggressiveness.csv', encoding = 'utf-8')
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

y = df["Category"]
vect = CountVectorizer(stop_words = 'english')
X_train_matrix = vect.fit_transform(df["newText"])

X_train, X_test, y_train, y_test = train_test_split(X_train_matrix, y, test_size= 0.3)
model = MultinomialNB()
model.fit(X_train, y_train)
# print (model.score(X_train, y_train))
# print (model.score(X_test, y_test))
predicted_result = model.predict(X_test)
print("\n")

joblib.dump(model,'model.pkl')
joblib.dump(vect,'vectorizer.pkl')