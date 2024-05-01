from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint


def get_songs_form_web(date):
    URL = f"https://www.billboard.com/charts/hot-100/{date}"
    respond = requests.get(URL)
    billboard_list = respond.text
    soup = BeautifulSoup(billboard_list, "html.parser")
    song_titles = soup.select('li ul li h3')
    song_list = []
    for song in song_titles:
        song_list.append(song.get_text(strip=True))
    return song_list


def get_spotify_uris(song_list, year):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="http://example.com",
            client_id="YOUR CLIENT ID",
            client_secret="YOUR CLIENT SECRET",
            show_dialog=True,
            cache_path="token.txt",
            username="YOUR NAME",
        )
    )

    user_id = sp.current_user()["id"]
    songs_URI = []
    for song in song_list:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]

            songs_URI.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")

        pprint.pp(songs_URI)

    return songs_URI, user_id


def create_playlist_from_song_list(song_uris, user_id, playlist_name):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="http://example.com",
            client_id="YOUR CLIENT ID",
            client_secret="YOUR CLIENT SECRET",
            show_dialog=True,
            cache_path="token.txt",
            username="YOUR NAME",
        )
    )
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)


date = "2009-07-18"
song_list = get_songs_form_web(date)
year = "2009"
song_uris, user_id = get_spotify_uris(song_list, year)
create_playlist_from_song_list(song_uris, user_id, f"billboards hot 100s {date}")
