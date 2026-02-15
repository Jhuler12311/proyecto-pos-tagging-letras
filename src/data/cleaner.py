import pandas as pd
import re
import os


def limpiar_texto(texto):
    if not isinstance(texto, str):
        return ""

    # 1. Convertir a minúsculas
    texto = texto.lower()

    # 2. Eliminar etiquetas de estructura (ej: [Chorus], [Intro], (Verse))
    texto = re.sub(r'\[.*?\]', '', texto)
    texto = re.sub(r'\(.*?\)', '', texto)

    # 3. Eliminar caracteres especiales, números y puntuación
    # Mantenemos letras y espacios
    texto = re.sub(r'[^a-záéíóúñ\s]', '', texto)

    # 4. Eliminar espacios múltiples y saltos de línea
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto


def ejecutar_limpieza():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_entrada = os.path.join(base_dir, 'data', 'processed', 'dataset_final.csv')
    ruta_salida = os.path.join(base_dir, 'data', 'processed', 'dataset_limpio.csv')

    if not os.path.exists(ruta_entrada):
        raise FileNotFoundError(f"No se encontró el archivo para limpieza: {ruta_entrada}")
        return

    print("LIMPIANDO")
    df = pd.read_csv(ruta_entrada)

    # Aplicamos la función mágica de limpieza
    df['lyric_clean'] = df['lyric'].apply(limpiar_texto)

    # Quitamos filas que hayan quedado vacías por error
    df = df[df['lyric_clean'] != ""]

    # Guardamos el resultado
    df.to_csv(ruta_salida, index=False)
    print(f"FINALIZADO, GUARDADO EN: {ruta_salida}")
    print(f"Muestra:\n{df['lyric_clean'].iloc[0][:100]}...")


if __name__ == "__main__":
    try:
        ejecutar_limpieza()
    except Exception as e:
        print(f" Error en cleaner.py: {e}")
