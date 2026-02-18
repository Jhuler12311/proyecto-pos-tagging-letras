import pandas as pd
import spacy
import nltk
from nltk.corpus import stopwords
import os
import time
from tqdm import tqdm
import re  # Para detección simple de idioma

# --- REQUISITOS TÉCNICOS (Criterio 1: Implementación) ---
try:
    nlp_es = spacy.load("es_core_news_sm")
    nlp_en = spacy.load("en_core_web_sm")
except:
    print("Asegúrate de instalar los modelos:")
    print("python -m spacy download es_core_news_sm")
    print("python -m spacy download en_core_web_sm")
    exit(1)

# Función auxiliar para detectar idioma aproximado
def detectar_idioma(texto):
    texto = str(texto).lower()
    en_words = len(re.findall(r'\b(the|you|love|i|me|my|your|it|to|in|on)\b', texto))
    es_words = len(re.findall(r'\b(el|la|los|me|mi|tu|te|amor|corazón|en|de)\b', texto))
    if en_words > es_words + 2:
        return 'en'
    elif es_words > en_words + 2:
        return 'es'
    return 'es'


def analizar_corpus_completo(return_df: bool = False):
    """
    Analizador morfosintáctico principal del proyecto.

    - Aplica POS Tagging (spaCy Universal POS)
    - Extrae métricas léxicas y morfológicas
    - Soporta corpus bilingüe (es/en)
    - Genera dataset maestro para visualización y análisis

    Parámetros
    ----------
    return_df : bool
        Si True, devuelve el DataFrame analizado para uso en otros módulos
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_entrada = os.path.join(base_dir, 'data', 'processed', 'dataset_limpio.csv')
    ruta_salida = os.path.join(base_dir, 'data', 'processed', 'dataset_master.csv')

    if not os.path.exists(ruta_entrada):
        raise FileNotFoundError(f"No se encontró dataset_limpio.csv en: {ruta_entrada}")

    print("Iniciando Pipeline Unificado (Tokenización, POS, Lemas)...")
    df = pd.read_csv(ruta_entrada)

    df_muestra = df.copy()
    textos = df_muestra['lyric_clean'].astype(str).tolist()

    resultados = []

    print("Analizando estructura morfosintáctica y emocionalidad...")

    for idx, texto in enumerate(tqdm(textos, desc="Procesando letras")):
        idioma = detectar_idioma(texto)
        nlp = nlp_en if idioma == 'en' else nlp_es
        doc = nlp(texto)

        # Lemas clave
        lemas_clave = [
            t.lemma_ for t in doc
            if not t.is_stop and not t.is_punct and t.pos_ in ['NOUN', 'ADJ', 'VERB']
        ]

        # Conteo POS
        v = len([t for t in doc if t.pos_ == "VERB"])
        s = len([t for t in doc if t.pos_ == "NOUN"])
        a = len([t for t in doc if t.pos_ == "ADJ"])
        p = len([t for t in doc if t.pos_ == "PRON"])

        # Métricas derivadas
        n_tokens = len(doc)
        densidad = (s + v + a) / n_tokens if n_tokens > 0 else 0
        ratio_sv = s / v if v > 0 else 0
        ratio_adj = a / n_tokens if n_tokens > 0 else 0

        resultados.append({
            'verbos': v,
            'sustantivos': s,
            'adjetivos': a,
            'pronombres_count': p,
            'densidad_lexica': densidad,
            'ratio_sust_verb': ratio_sv,
            'ratio_adjetivos': ratio_adj,
            'palabras_clave': ", ".join(lemas_clave[:12]),
            'adjetivos_ejemplo': ", ".join([t.text for t in doc if t.pos_ == "ADJ"][:8]),
            'idioma_detectado': idioma
        })

    df_analizado = pd.DataFrame(resultados)
    df_final = pd.concat([df_muestra.reset_index(drop=True), df_analizado], axis=1)

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    df_final.to_csv(ruta_salida, index=False)

    print("\nPipeline Finalizado.")
    print(f"Archivo maestro generado: {ruta_salida}")
    print(f"Filas procesadas: {len(df_final)}")
    print(f"Columnas finales: {list(df_final.columns)}")

    if return_df:
        return df_final


if __name__ == "__main__":
    try:
        analizar_corpus_completo()
    except Exception as e:
        print(f"Error en analyser.py: {e}")
