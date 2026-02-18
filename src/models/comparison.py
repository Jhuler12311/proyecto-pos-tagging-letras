import os
import time
import csv
from collections import defaultdict


def ejecutar_comparacion_y_metricas():
    # Rutas de archivos
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_entrada = os.path.join(base_dir, 'data', 'processed', 'dataset_limpio.csv')
    ruta_salida = os.path.join(base_dir, 'data', 'processed', 'dataset_avanzado.csv')

    if not os.path.exists(ruta_entrada):
        raise FileNotFoundError(f"No se encontró dataset_limpio.csv en: {ruta_entrada}")

    print(" Iniciando comparación avanzada...")

    resultados = []
    acumulado_tokens = defaultdict(int)

    # Leer CSV manualmente
    with open(ruta_entrada, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i >= 5000:  # Limitamos a 5000 registros como en el original
                break

            texto = str(row.get('lyric_clean', ''))

            # Análisis básico de texto
            palabras = texto.split()
            n_tokens = len(palabras)

            # Métricas simplificadas
            resultados.append({
                'tokens': n_tokens,
                'caracteres': len(texto),
                'palabras_unicas': len(set(palabras))
            })

            # Conteo de palabras
            for palabra in palabras:
                acumulado_tokens[palabra] += 1

    # Guardar resultados
    campos = ['tokens', 'caracteres', 'palabras_unicas']

    with open(ruta_salida, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=campos)
        writer.writeheader()
        for resultado in resultados:
            writer.writerow(resultado)

    # Guardar estadísticas de tokens
    ruta_tokens = os.path.join(base_dir, 'data', 'processed', 'estadisticas_tokens.csv')
    with open(ruta_tokens, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['token', 'frecuencia'])
        for token, freq in sorted(acumulado_tokens.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([token, freq])

    print("\n Pipeline completado")
    print(f" Estadísticas guardadas en: {ruta_salida}")
    print(f" Análisis de tokens guardado en: {ruta_tokens}")


if __name__ == "__main__":
    try:
        ejecutar_comparacion_y_metricas()
    except Exception as e:
        print(f" Error en comparison.py: {e}")