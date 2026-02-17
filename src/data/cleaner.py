import csv
import re
import os


def limpiar_texto(texto):
    if not isinstance(texto, str):
        return ""

    # 1. Convertir a minúsculas
    texto = texto.lower()

    # 2. Eliminar etiquetas de estructura
    texto = re.sub(r'\[.*?\]', '', texto)
    texto = re.sub(r'\(.*?\)', '', texto)

    # 3. Eliminar caracteres especiales, números y puntuación
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

    print("LIMPIANDO")
    
    # Leer el CSV usando la biblioteca estándar
    datos = []
    with open(ruta_entrada, 'r', encoding='utf-8') as archivo_entrada:
        lector = csv.DictReader(archivo_entrada)
        for fila in lector:
            texto_limpio = limpiar_texto(fila['lyric'])
            if texto_limpio:  # Solo incluir si no está vacío
                fila['lyric_clean'] = texto_limpio
                datos.append(fila)

    # Guardar el resultado
    if datos:
        with open(ruta_salida, 'w', encoding='utf-8', newline='') as archivo_salida:
            escritor = csv.DictWriter(archivo_salida, fieldnames=datos[0].keys())
            escritor.writeheader()
            escritor.writerows(datos)
        
        print(f"FINALIZADO, GUARDADO EN: {ruta_salida}")
        if datos:
            print(f"Muestra:\n{datos[0]['lyric_clean'][:100]}...")
    else:
        print("No se encontraron datos válidos para procesar")


if __name__ == "__main__":
    try:
        ejecutar_limpieza()
    except Exception as e:
        print(f"Error en cleaner.py: {e}")