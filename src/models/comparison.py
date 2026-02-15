import pandas as pd
import spacy
import nltk
import os
import time
from nltk.tokenize import word_tokenize

# --- REQUISITOS TÉCNICOS (Criterio 1: Implementación) ---
try:
    # Cargamos modelos para Español e Inglés para evitar errores con artistas internacionales
    nlp_es = spacy.load("es_core_news_sm")
    nlp_en = spacy.load("en_core_web_sm")
except:
    print("Asegúrate de instalar los modelos: python -m spacy download es_core_news_sm en_core_web_sm")

def ejecutar_comparacion_y_metricas():
    # Rutas de archivos
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_entrada = os.path.join(base_dir, 'data', 'processed', 'dataset_limpio.csv')
    ruta_salida = os.path.join(base_dir, 'data', 'processed', 'dataset_avanzado.csv')

    if not os.path.exists(ruta_entrada):
        raise FileNotFoundError(f"No se encontró dataset_limpio.csv en: {ruta_entrada}")

    # Cargar spaCy
    try:
        nlp = spacy.load("es_core_news_sm")
    except OSError:
        raise OSError("Modelo es_core_news_sm no instalado. Ejecuta: python -m spacy download es_core_news_sm")

    print(" Iniciando comparación avanzada NLTK vs spaCy...")
    df = pd.read_csv(ruta_entrada)

    df_muestra = df.head(5000).copy()
    resultados = []

    # Acumuladores globales de etiquetas
    acumulado_spacy = {}
    acumulado_nltk = {}

    for index, fila in df_muestra.iterrows():
        texto = str(fila['lyric_clean'])

        # 1️ spaCy
        start_sp = time.time()
        # Detección simple por presencia de palabras comunes
        if any(palabra in texto.lower() for palabra in ["the", "and", "love", "baby"]):
            doc = nlp_en(texto)
        else:
            doc = nlp_es(texto)
        t_spacy = time.time() - start_sp

        # 2️ NLTK
        start_nl = time.time()
        tokens_nltk = word_tokenize(texto)
        tags_nltk = nltk.pos_tag(tokens_nltk)
        t_nltk = time.time() - start_nl

        #Conteo spaCy (Universal POS)
        conteo_spacy = {}
        for token in doc:
            conteo_spacy[token.pos_] = conteo_spacy.get(token.pos_, 0) + 1

        #Conteo NLTK (Penn Treebank)
        conteo_nltk = {}
        for palabra, etiqueta in tags_nltk:
            conteo_nltk[etiqueta] = conteo_nltk.get(etiqueta, 0) + 1

        #Acumular resultados globales
        for k, v in conteo_spacy.items():
            acumulado_spacy[k] = acumulado_spacy.get(k, 0) + v

        for k, v in conteo_nltk.items():
            acumulado_nltk[k] = acumulado_nltk.get(k, 0) + v

        # 3️ Métricas morfológicas
        n_tokens = len(doc)
        v = len([t for t in doc if t.pos_ == "VERB"])
        s = len([t for t in doc if t.pos_ == "NOUN"])
        a = len([t for t in doc if t.pos_ == "ADJ"])
        p = len([t for t in doc if t.pos_ == "PRON"])

        densidad = (s + v + a) / n_tokens if n_tokens > 0 else 0
        ratio_sv = s / v if v > 0 else 0

        resultados.append({
            'verbos': v,
            'sustantivos': s,
            'adjetivos': a,
            'pronombres': p,
            'densidad_lexica': densidad,
            'ratio_sust_verb': ratio_sv,
            'tiempo_spacy': t_spacy,
            'tiempo_nltk': t_nltk
        })

    # Consolidar métricas por canción
    df_res = pd.DataFrame(resultados)
    df_final = pd.concat([df_muestra.reset_index(drop=True), df_res], axis=1)

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    df_final.to_csv(ruta_salida, index=False)

    #Crear tabla comparativa de etiquetas
    df_compare = pd.DataFrame({
        "spaCy_Universal": pd.Series(acumulado_spacy),
        "NLTK_PennTreebank": pd.Series(acumulado_nltk)
    }).fillna(0)

    ruta_comparacion = os.path.join(base_dir, 'data', 'processed', 'comparacion_etiquetas.csv')
    df_compare.to_csv(ruta_comparacion)

    # Resultados finales
    promedio_spacy = df_res['tiempo_spacy'].mean()
    promedio_nltk = df_res['tiempo_nltk'].mean()

    print("\n Pipeline completado")
    print(f"Promedio Tiempo spaCy: {promedio_spacy:.5f}s")
    print(f"Promedio Tiempo NLTK: {promedio_nltk:.5f}s")
    print(f" Tabla comparativa guardada en: {ruta_comparacion}")

    # Conlusion
    if promedio_spacy < promedio_nltk:
        print(" Conclusión: spaCy demuestra mayor eficiencia computacional.")
    else:
        print("Conclusión: NLTK mostró mejor rendimiento (caso poco común).")


if __name__ == "__main__":
    try:
        ejecutar_comparacion_y_metricas()
    except Exception as e:
        print(f" Error en comparison.py: {e}")
