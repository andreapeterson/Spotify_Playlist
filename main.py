from bs4 import BeautifulSoup
import requests
import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth


### SET-UP
date = input("What day would you like a Spotify playlist? Type answer in this format: YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

### SONGS INTO LIST
songs = [song.text.strip() for song in soup.select(selector="li h3", id="title-of-a-story")]
print(songs)


###  SPOTIFY AUTHENTICATION
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.ID,
                                               client_secret=config.SECRET,
                                               redirect_uri="http://example.com/",
                                               scope="playlist-modify-private" ))
results = sp.current_user()
id = results["id"]

### USING SPOTIPY TO SEARCH FOR SONGS BY TITLE
song_uris = []
year = date.split("-")[0]

print("\nCalculating URI'S...\n")
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

### USING SPOTIPY TO CREATE PLAYLIST
playlist_name = input("\n\n\n\n\nWhat do you want to call this playlist? ")
playlist = sp.user_playlist_create(user=id, name=playlist_name, public=False, description=f"Top 100 songs on {date}")
playlist_id = playlist["id"]

### USING SPOTIPY TO ADD SONGS TO PLAYLIST
sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
