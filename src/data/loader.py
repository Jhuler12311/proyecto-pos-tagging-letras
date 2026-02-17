import csv
import os
import re
import random
from collections import defaultdict

def procesar_letras_proyecto():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_entrada = os.path.join(base_dir, 'data', 'raw', 'tcc_ceds_music.csv')
    ruta_salida = os.path.join(base_dir, 'data', 'processed', 'dataset_final.csv')

    if not os.path.exists(ruta_entrada):
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {ruta_entrada}")

    print("CARGANDO DATASET ORIGINAL...")
    
    # Leer CSV manualmente
    datos = []
    encabezados = []
    with open(ruta_entrada, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        encabezados = [c.lower() for c in next(reader)]  # Normalizar columnas a minúsculas
        datos = list(reader)

    # Detectar nombres correctos de columnas
    col_artista = encabezados.index('artist_name' if 'artist_name' in encabezados else 'artist')
    col_letra = encabezados.index('lyrics' if 'lyrics' in encabezados else 'lyric')
    col_anio = encabezados.index('release_date' if 'release_date' in encabezados else 'year')

    def extraer_anio(valor):
        try:
            if isinstance(valor, str):
                match = re.search(r'\b(19\d{2}|20\d{2})\b', valor)
                if match:
                    return int(match.group(0))
            return int(float(valor)) if valor else None
        except:
            return None

    def obtener_decada(year):
        if not year:
            return "Unknown"
        try:
            y = int(year)
            return f"{(y // 10) * 10}s"
        except:
            return "Unknown"

    # Procesar datos
    datos_procesados = []
    for fila in datos:
        year_clean = extraer_anio(fila[col_anio])
        decade = obtener_decada(year_clean)
        
        datos_procesados.append({
            'artist': fila[col_artista],
            'lyric': fila[col_letra],
            'year_original': fila[col_anio],
            'year': year_clean,
            'decade': decade
        })

    print(f"Total de canciones disponibles: {len(datos_procesados)}")

    # Muestra aleatoria
    if len(datos_procesados) > 10000:
        df_final = random.sample(datos_procesados, 10000)
    else:
        df_final = datos_procesados

    print(f"Total de canciones en la muestra final: {len(df_final)}")

    # Guardar el dataset final en formato CSV
    with open(ruta_salida, 'w', encoding='utf-8', newline='') as file:
        columnas = ['artist', 'lyric', 'year_original', 'year', 'decade']
        writer = csv.DictWriter(file, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(df_final)

    print(f"Dataset completo guardado en: {ruta_salida}")

    # Calcular y mostrar la distribución temporal
    distribucion_temporal = defaultdict(int)
    for row in df_final:
        distribucion_temporal[row['decade']] += 1

    print("\n--- Distribución Temporal (después de muestreo) ---")
    for decada in sorted(distribucion_temporal.keys()):
        print(f"{decada}: {distribucion_temporal[decada]}")

if __name__ == "__main__":
    try:
        procesar_letras_proyecto()
    except Exception as e:
        print(f"Error en loader.py: {e}")