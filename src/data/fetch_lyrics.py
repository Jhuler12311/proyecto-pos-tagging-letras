import requests
import os
import time
import csv
import re
from my_secrets import GENIUS_TOKEN
from bs4 import BeautifulSoup


def verificar_directorios():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    ruta_processed = os.path.join(base_dir, "data", "processed")
    ruta_archivo = os.path.join(ruta_processed, "my_artists.csv")
    os.makedirs(ruta_processed, exist_ok=True)
    return ruta_archivo


def buscar_id_artista(artist_name):
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    params = {"q": artist_name}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            for hit in data["response"]["hits"]:
                if hit["result"]["primary_artist"]["name"].lower() == artist_name.lower():
                    return hit["result"]["primary_artist"]["id"]
    except:
        return None
    return None


def obtener_url_cancion(song_id):
    url = f"https://api.genius.com/songs/{song_id}"
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["response"]["song"]["url"]
    except:
        return None
    return None


def extraer_letras(url_cancion):
    if not url_cancion:
        return "No disponible"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url_cancion, headers=headers, timeout=15)
        if response.status_code != 200:
            return "Error de conexion"

        soup = BeautifulSoup(response.text, "html.parser")
        contenedores = soup.find_all("div", attrs={"data-lyrics-container": "true"})

        if contenedores:
            texto = "\n".join([c.get_text(separator="\n") for c in contenedores])
        else:
            contenedor_lyrics = soup.find("div", class_="lyrics")
            if contenedor_lyrics:
                texto = contenedor_lyrics.get_text()
            else:
                return "Letras no encontradas"

        texto_limpio = re.sub(r'\[.*?\]', '', texto)
        return texto_limpio.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def obtener_letras_artista(artist_id, artist_name, max_songs=10):
    canciones = []
    url = f"https://api.genius.com/artists/{artist_id}/songs"
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    params = {"per_page": 20, "sort": "popularity", "page": 1}

    while len(canciones) < max_songs:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200: break
        songs = response.json()["response"]["songs"]
        if not songs: break

        for song in songs:
            if len(canciones) >= max_songs: break
            if song['primary_artist']['id'] != artist_id: continue

            url_s = obtener_url_cancion(song['id'])
            lyrics = extraer_letras(url_s)

            if "Letras no encontradas" not in lyrics and len(lyrics) > 100:
                anio = song.get("release_date_components", {}).get("year", 2024)

                # Reporte en consola
                print(f"---")
                print(f"Cancion: {song['title']}")
                print(f"Caracteres: {len(lyrics)}")
                print(f"Vista previa: {lyrics[:50].replace(chr(10), ' ')}...")

                canciones.append({
                    "artist": artist_name,
                    "track_name": song["title"],
                    "year_original": anio,
                    "genre": "custom",
                    "lyric": lyrics,
                    "year": anio
                })
            else:
                print(f"Salteada: {song['title']} (Sin letra o muy corta)")

            time.sleep(1.5)

        params["page"] += 1
    return canciones


def descargar_mis_artistas(artistas, max_por_artista=10):
    todas = []
    for artista in artistas:
        print(f"Iniciando busqueda de: {artista}")
        a_id = buscar_id_artista(artista)
        if a_id:
            canciones = obtener_letras_artista(a_id, artista, max_por_artista)
            todas.extend(canciones)

    if todas:
        ruta = verificar_directorios()
        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=todas[0].keys())
            writer.writeheader()
            writer.writerows(todas)
        print(f"\nFinalizado: {len(todas)} canciones guardadas en {ruta}")


if __name__ == "__main__":
    descargar_mis_artistas(["PXNDX"], max_por_artista=10)