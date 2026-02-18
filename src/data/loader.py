import pandas as pd
import os
import re

def procesar_letras_proyecto(return_df: bool = False):
    """
    Loader del proyecto.
    - Carga el dataset crudo
    - Limpia y normaliza columnas
    - Extrae año y década
    - Genera dataset base para POS Tagging

    Parámetros
    ----------
    return_df : bool
        Si True, devuelve el DataFrame procesado para uso en otros módulos
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_entrada = os.path.join(base_dir, 'data', 'raw', 'tcc_ceds_music.csv')
    ruta_salida = os.path.join(base_dir, 'data', 'processed', 'dataset_final.csv')

    if not os.path.exists(ruta_entrada):
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {ruta_entrada}")

    print("CARGANDO DATASET ORIGINAL...")
    df = pd.read_csv(ruta_entrada)

    # Normalizar columnas a minúsculas
    df.columns = [c.lower() for c in df.columns]

    # Detectar nombres correctos
    col_artista = 'artist_name' if 'artist_name' in df.columns else 'artist'
    col_letra = 'lyrics' if 'lyrics' in df.columns else 'lyric'
    col_anio = 'release_date' if 'release_date' in df.columns else 'year'

    # Función robusta para extraer año
    def extraer_anio(valor):
        try:
            if isinstance(valor, str):
                match = re.search(r'\b(19\d{2}|20\d{2})\b', valor)
                if match:
                    return int(match.group(0))
            if pd.notna(valor):
                return int(float(valor))
        except:
            pass
        return None

    print(f"Columna de año detectada: {col_anio}")
    df['year_clean'] = df[col_anio].apply(extraer_anio)
    print("Años válidos después de limpieza:", df['year_clean'].notna().sum())
    print("Años únicos encontrados:", sorted(df['year_clean'].dropna().unique()))

    # Crear década
    def obtener_decada(year):
        if pd.isna(year):
            return "Unknown"
        try:
            y = int(year)
            return f"{(y // 10) * 10}s"
        except:
            return "Unknown"

    df['decade'] = df['year_clean'].apply(obtener_decada)

    print(f"Total de canciones disponibles: {len(df)}")

    # Muestreo controlado
    if len(df) > 10000:
        df_final = df.sample(n=10000, random_state=42).copy()
    else:
        df_final = df.copy()

    # Renombrar columnas clave
    df_final = df_final.rename(columns={
        col_artista: 'artist',
        col_letra: 'lyric',
        col_anio: 'year_original',
        'year_clean': 'year'
    })

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    df_final.to_csv(ruta_salida, index=False)

    print(f"Dataset completo guardado en: {ruta_salida}")
    print("\n--- Distribución Temporal (después de muestreo) ---")
    print(df_final['decade'].value_counts().sort_index())

    if return_df:
        return df_final


if __name__ == "__main__":
    try:
        procesar_letras_proyecto()
    except Exception as e:
        print(f"Error en loader.py: {e}")
