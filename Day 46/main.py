from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
REDIRECT_URL=os.getenv("REDIRECT_URL")
USERNAME=os.getenv("USERNAME")

scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=USERNAME,))

user_id = sp.current_user()["id"]

date=input("Which day you want to travel to? Type date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"
HEADER = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 OPR/123.0.0.0"
}
response = requests.get(url=URL, headers=HEADER)
response.raise_for_status()
soup=BeautifulSoup(response.text, "html.parser")

songs = soup.select("li ul li h3")

playlist = sp.user_playlist_create(user_id, f"Billboard 100: {date}", public=False, description='')
tracks = []
for s in songs:
    s_str=s.string.strip()
    track=sp.search(q=f"track:{s_str} year:{date.split("-")[0]}", type="track")
    try:
        track_uri = track["tracks"]["items"][0]["uri"]
        tracks.append(track_uri)
    except IndexError:
        print(f"{s_str} doesn't exist in Spotify.")
sp.playlist_add_items(playlist_id=playlist["id"], items=tracks, position=0)

