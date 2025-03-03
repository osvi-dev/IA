import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import speech_recognition as sr
from gtts import gTTS

# Función para cargar preguntas desde un archivo
def CargaPreguntas(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        texto = f.read()
    pregs = sent_tokenize(texto)
    return texto, pregs

# Función para eliminar stopwords y caracteres no alfabéticos
def getCleanQs(listaOracion):
    stopws = stopwords.words("spanish")
    textoconsw = [w.lower() for w in listaOracion if w.isalpha()]
    textosinsw = [w for w in textoconsw if w not in stopws]
    return textosinsw

# Función para crear vectores de palabras
def crearVector(oracion, diccionario):
    distrib = nltk.FreqDist(oracion)
    vector = [distrib[w] for w in diccionario]
    return vector

# Función para cargar respuestas desde un archivo
def cargaRespuesta(archivo, indice):
    with open(archivo, "r", encoding="utf-8") as f:
        texto = f.read()
    res = sent_tokenize(texto)
    return res[indice] if indice < len(res) else "No tengo una respuesta para eso."

# Función principal del chatbot
def chatbot(pu):
    (ptxt, psucias) = CargaPreguntas("preg.txt")
    qsWords = [word_tokenize(orac) for orac in psucias]
    tssw = [getCleanQs(orac) for orac in qsWords]
    texto_tot = getCleanQs(word_tokenize(ptxt) + word_tokenize(pu))
    dicc = set(texto_tot)
    vs = [crearVector(ora, dicc) for ora in tssw]
    vpu = crearVector(getCleanQs(word_tokenize(pu)), dicc)
    sims = [((cosine_distance(vpu, v) - 1) * (-1)) for v in vs]
    indice = sims.index(max(sims))
    return cargaRespuesta("res.txt", indice)

# Función para reconocimiento de voz
def reconocer_voz():
    voz = sr.Recognizer()
    print('Escuchando... ')
    with sr.Microphone() as fuente:
        voz.adjust_for_ambient_noise(fuente)
        audio = voz.listen(fuente)
        try:
            texto = voz.recognize_google(audio, language="es-ES")
            print('\nTexto reconocido: ', texto)
            return texto
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return None
        except sr.RequestError as e:
            print(f"Error al solicitar resultados del servicio de reconocimiento de voz; {e}")
            return None

# Función para sintetizar y reproducir la respuesta
def hablar(respuesta):
    tts = gTTS(respuesta, lang='es')
    tts.save("respuesta.mp3")
    os.system("mpg123 -q respuesta.mp3")

# Ejecución principal
if __name__ == "__main__":
    while True:
        texto_usuario = reconocer_voz()
        if texto_usuario:
            respuesta = chatbot(texto_usuario)
            print("Chatbot:", respuesta)
            hablar(respuesta)
