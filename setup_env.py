import nltk
import spacy


def setup_nltk():
    print("Descargando recursos NLTK...")
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')


def check_spacy_models():
    modelos = ["es_core_news_sm", "en_core_web_sm"]

    for modelo in modelos:
        try:
            spacy.load(modelo)
            print(f"Modelo {modelo} ya instalado.")
        except OSError:
            print(f"Modelo {modelo} no encontrado.")
            print(f"Instálalo con:")
            print(f"python -m spacy download {modelo}")


if __name__ == "__main__":
    setup_nltk()
    check_spacy_models()
