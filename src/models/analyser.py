import nltk
import os
import time
import re
from collections import defaultdict
import csv
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Descargar recursos necesarios de NLTK
try:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('universal_tagset')
except:
    print("Error al descargar recursos de NLTK")
    exit(1)

def detectar_idioma(texto):
    texto = str(texto).lower()
    en_words = len(re.findall(r'\b(the|you|love|i|me|my|your|it|to|in|on)\b', texto))
    es_words = len(re.findall(r'\b(el|la|los|me|mi|tu|te|amor|corazón|en|de)\b', texto))
    if en_words > es_words + 2:
        return 'en'
    elif es_words > en_words + 2:
        return 'es'
    return 'es'

def analizar_texto(texto, idioma='es'):
    tokens = word_tokenize(texto)
    if idioma == 'en':
        return pos_tag(tokens, tagset='universal')
    else:
        # Para español, usamos el mismo etiquetador pero con consciencia del idioma
        return pos_tag(tokens, tagset='universal')

def leer_csv(ruta):
    datos = []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)

def escribir_csv(ruta, datos, fieldnames):
    with open(ruta, 'w', encoding='utf-8', newline='') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
        escritor.writeheader()
        escritor.writerows(datos)

def analizar_corpus_completo():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_entrada = os.path.join(base_dir, 'data', 'processed', 'dataset_limpio.csv')
    # Completar el resto de la función según tus necesidades