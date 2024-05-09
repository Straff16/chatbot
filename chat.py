import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer

warnings.filterwarnings('ignore')
nltk.download("popular", quiet=True)

f = open('napo.txt', 'r', errors='ignore')
raw = f.read()
raw = raw.lower()
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Lista de stop words en español proporcionada por NLTK
spanish_stop_words = nltk.corpus.stopwords.words('spanish')

GREETING_INPUTS = ("hola", "hi", "greetings", "sup", "qué tal","hey","yo")
GREETING_RESPONSES = ["¡Hola!", "¡Hola, ¿cómo estás?", "¡Hola, me alegra verte!", "¡Hola, ¿qué tal?", "¡Hola, estoy aquí para ayudarte!"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    spar_response=""
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=spanish_stop_words)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf==0:
        spar_response="Lo siento, no te entiendo"
    else:
        spar_response = spar_response+sent_tokens[idx]
    return spar_response

def know_about(topic):
    if "napoleon" in topic.lower() or "bonaparte" in topic.lower():
        return "Sé mucho sobre Napoleón Bonaparte. ¿Qué te gustaría saber sobre él?"
    else:
        return "Lo siento, no estoy familiarizado con ese tema."

flag=True
print("Spar: Mi nombre es Spar. Responderé tus preguntas sobre Chatbots. Si quieres salir, escribe Adiós.")
while(flag==True):
        user_response = input()
        user_response=user_response.lower()
        if(user_response!='adiós'):
            if(user_response=="gracias" or user_response=='gracias' ):
                flag=False
                print('Spar: ¡De nada!')
            elif greeting(user_response)!=None:
                print('Spar: '+greeting(user_response))
            elif "saber sobre" in user_response:
                print('Spar: '+know_about(user_response))
            else:
                print('Spar: ',end='')
                print(response(user_response))
                sent_tokens.remove(user_response)
        else:
            flag=False


''' plan b
import wikipedia

# Función para obtener el contenido de un artículo de Wikipedia
def get_wikipedia_content(topic):
    wikipedia.set_lang("es")  # Establecer el idioma de la búsqueda en español
    try:
        page = wikipedia.page(topic)
        return page.content
    except wikipedia.exceptions.PageError as e:
        return "Lo siento, no pude encontrar información sobre eso."

# Obtener el contenido del artículo de Wikipedia
topic = "Napoleón Bonaparte"  # Tema que quieres buscar en Wikipedia
wikipedia_content = get_wikipedia_content(topic)

# Convertir el contenido a minúsculas si es necesario
if wikipedia_content:
    wikipedia_content = wikipedia_content.lower()
    # Aquí puedes realizar cualquier procesamiento adicional que necesites con el contenido de Wikipedia
else:
    print("No se pudo obtener contenido de Wikipedia para el tema especificado.")

'''