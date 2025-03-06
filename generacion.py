import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import speech_recognition as sr
from gtts import gTTS
from numpy import isnan

# Cargar preguntas desde un archivo
def CargaPreguntas(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        pregs = f.read().splitlines()  # Corrección: usar splitlines() en vez de sent_tokenize()
    return pregs

# Cargar respuestas desde un archivo
def cargaRespuesta(archivo, indice):
    with open(archivo, "r", encoding="utf-8") as f:
        res = f.read().splitlines()  # Corrección: usar splitlines()
    return res[indice] if indice < len(res) else "No tengo una respuesta para eso."

# Eliminar stopwords y caracteres no alfabéticos
def getCleanQs(listaOracion):
    stopws = stopwords.words("spanish")
    textoconsw = [w.lower() for w in listaOracion if w.isalpha()]
    textosinsw = [w for w in textoconsw if w not in stopws]
    return textosinsw

# Crear vectores de palabras
def crearVector(oracion, diccionario):
    if not oracion:  # Manejar caso de oración vacía
        return [0] * len(diccionario)
    distrib = nltk.FreqDist(oracion)
    vector = [distrib[w] for w in diccionario]
    return vector

# Chatbot mejorado
def chatbot(pu):
    psucias = CargaPreguntas("preg.txt")
    qsWords = [word_tokenize(orac) for orac in psucias]
    tssw = [getCleanQs(orac) for orac in qsWords]

    # Crear diccionario solo con palabras limpias de las preguntas
    dicc = set(word for oracion in tssw for word in oracion)

    vs = [crearVector(ora, dicc) for ora in tssw]
    vpu = crearVector(getCleanQs(word_tokenize(pu)), dicc)

    if sum(vpu) == 0:  # Si el vector del usuario está vacío, evitar cálculo erróneo
        return "Lo siento, no entendí la pregunta."

    # Calcular la similitud de coseno
    sims = [1 - cosine_distance(vpu, v) if not isnan(cosine_distance(vpu, v)) else 0 for v in vs]

    if max(sims) < 0.3:  # Umbral mínimo de similitud
        return "Lo siento, no entendí la pregunta."

    indice = sims.index(max(sims))
    return cargaRespuesta("res.txt", indice)

# Reconocimiento de voz
def reconocer_voz():
    voz = sr.Recognizer()
    print('Escuchando... ')
    with sr.Microphone(device_index=5) as fuente:
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

# Sintetizar y reproducir respuesta
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
