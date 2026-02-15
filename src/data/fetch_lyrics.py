import requests
import os
import time
import csv
from secrets import GENIUS_TOKEN
from bs4 import BeautifulSoup


def verificar_directorios():
    directorio_actual = os.getcwd()
    print(f"Directorio actual: {directorio_actual}")

    ruta_data = os.path.join(directorio_actual, "data")
    ruta_processed = os.path.join(ruta_data, "processed")
    ruta_archivo = os.path.join(ruta_processed, "my_artists.csv")

    os.makedirs(ruta_processed, exist_ok=True)
    print(f"Directorio processed creado/listo: {ruta_processed}")

    return ruta_archivo


def buscar_id_artista(artist_name):
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    params = {"q": artist_name}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error búsqueda {artist_name}: {response.status_code}")
        return None

    data = response.json()
    for hit in data["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"].lower() == artist_name.lower():
            return hit["result"]["primary_artist"]["id"]

    print(f"No ID para {artist_name}")
    return None


def obtener_url_cancion(song_id):
    url = f"https://api.genius.com/songs/{song_id}"
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["response"]["song"]["url"]  # URL de la página web
    print(f"No URL para song {song_id}")
    return None


def extraer_letras(url_cancion):
    if not url_cancion:
        return "No disponible"

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url_cancion, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"Error HTTP {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        # Genius usa div con data-lyrics-container="true" para las letras
        lyrics_div = soup.find("div", attrs={"data-lyrics-container": "true"})

        if lyrics_div:
            # Limpieza básica: texto con saltos de línea
            lyrics_text = lyrics_div.get_text(separator="\n").strip()
            # Quitar [Verse 1], [Chorus] si quieres (opcional)
            # lyrics_text = re.sub(r'\[.*?\]', '', lyrics_text)
            return lyrics_text
        else:
            return "Letras no encontradas en HTML"
    except Exception as e:
        print(f"Error scraping {url_cancion}: {str(e)}")
        return "Error al scrapear letras"


def obtener_letras_artista(artist_id, artist_name, max_songs=10):
    canciones = []
    url = f"https://api.genius.com/artists/{artist_id}/songs"
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    params = {"per_page": 50, "sort": "popularity"}

    page = 1
    while len(canciones) < max_songs:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error página {page}: {response.status_code}")
            break

        data = response.json()
        songs = data["response"]["songs"]

        if not songs:
            break

        for song in songs:
            if len(canciones) >= max_songs:
                break

            song_url = obtener_url_cancion(song['id'])
            lyrics = extraer_letras(song_url)

            canciones.append({
                "artist": artist_name,
                "track_name": song["title"],
                "year": song.get("release_date_components", {}).get("year", None),
                "genre": "custom",
                "lyric": lyrics,
                "source": "my_artists"
            })

            print(f"  - {song['title']} → letras obtenidas ({len(lyrics)} caracteres)")

        page += 1
        time.sleep(2)  # Pausa más larga para evitar bloqueo

    return canciones


def descargar_mis_artistas(artistas, max_por_artista=8):
    todas_canciones = []

    for artista in artistas:
        print(f"\nBuscando {artista}...")
        artist_id = buscar_id_artista(artista)
        if artist_id:
            canciones = obtener_letras_artista(artist_id, artista, max_por_artista)
            todas_canciones.extend(canciones)
            print(f" → Descargadas {len(canciones)} canciones")
        time.sleep(3)

    if todas_canciones:
        ruta_salida = verificar_directorios()

        try:
            with open(ruta_salida, mode='w', newline='', encoding='utf-8') as archivo_csv:
                nombres_columnas = todas_canciones[0].keys()
                escritor_csv = csv.DictWriter(archivo_csv, fieldnames=nombres_columnas)
                escritor_csv.writeheader()
                for cancion in todas_canciones:
                    escritor_csv.writerow(cancion)

            print(f"\n¡Éxito! Guardadas {len(todas_canciones)} canciones en:\n{ruta_salida}")
            print(f"Tamaño: {os.path.getsize(ruta_salida)} bytes")
        except Exception as e:
            print(f"Error al guardar: {str(e)}")
    else:
        print("No se descargó ninguna canción.")


if __name__ == "__main__":
    mis_artistas = ["PXNDX", "Aventura"]  # agrega más
    descargar_mis_artistas(mis_artistas, max_por_artista=10)