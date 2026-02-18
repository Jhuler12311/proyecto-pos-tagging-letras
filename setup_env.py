import nltk
import spacy
import sys
import subprocess


def setup_nltk():
    print("Configurando NLTK...")
    resources = [
        'punkt',  # tokenización
        'stopwords',  # palabras vacías
        'averaged_perceptron_tagger'  # etiquetado POS
    ]

    for res in resources:
        try:
            nltk.download(res, quiet=True)
            print(f"✓ {res} descargado/instalado correctamente.")
        except Exception as e:
            print(f"Error al descargar {res}: {e}")
            print("Intenta manualmente: nltk.download('{res}') en Python")

    print("NLTK configurado.\n")


def check_spacy_models():
    print("Verificando modelos de spaCy...")
    modelos = {
        "es_core_news_sm": "Español (pequeño)",
        "en_core_web_sm": "Inglés (pequeño)"
    }

    for modelo, desc in modelos.items():
        try:
            spacy.load(modelo)
            print(f"✓ {modelo} ({desc}) ya está instalado.")
        except OSError:
            print(f"✗ {modelo} ({desc}) no encontrado.")
            print(f"Instalándolo automáticamente...")
            try:
                subprocess.check_call([sys.executable, "-m", "spacy", "download", modelo])
                print(f"   → Instalado correctamente.")
            except subprocess.CalledProcessError:
                print(f"   → Error al instalar automáticamente.")
                print(f"   Ejecuta manualmente: python -m spacy download {modelo}")

    print("\nspaCy listo.\n")


def main():
    print("=== Configuración del entorno para POS Tagging ===\n")
    setup_nltk()
    check_spacy_models()
    print("¡Entorno configurado! Puedes ejecutar loader.py, cleaner.py, analyser.py, etc.")
    print("Si ves errores de modelos faltantes, vuelve a correr este script.")


if __name__ == "__main__":
    main()