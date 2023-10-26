import sys
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch

# Try to read the client ID from client_id.txt
try:
    with open('client_id.txt', 'r') as file:
        SPOTIPY_CLIENT_ID = file.read().strip()
except FileNotFoundError:
    SPOTIPY_CLIENT_ID = input("Enter your Spotify Client ID: ")
    with open('client_id.txt', 'w') as file:
        file.write(SPOTIPY_CLIENT_ID)

# Try to read the client secret from client_secret.txt
try:
    with open('client_secret.txt', 'r') as file:
        SPOTIPY_CLIENT_SECRET = file.read().strip()
except FileNotFoundError:
    SPOTIPY_CLIENT_SECRET = input("Enter your Spotify Client Secret: ")
    with open('client_secret.txt', 'w') as file:
        file.write(SPOTIPY_CLIENT_SECRET)

def get_youtube_link(artist, track_name):
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    query = f"artist:{artist} track:{track_name}"
    results = sp.search(q=query, type='track', limit=1)

    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['id']
        track_info = sp.track(track_id)
        artist = track_info['artists'][0]['name']
        track_name = track_info['name']

        query = f"{artist} {track_name} official video"
        youtube_results = YoutubeSearch(query, max_results=1).to_dict()

        if youtube_results:
            youtube_link = f"https://www.youtube.com/watch?v={youtube_results[0]['id']}"
            return youtube_link
        else:
            return "No results found on YouTube."
    else:
        return "No results found on Spotify."

def main():
    while True:
        print("Spotify to YouTube / YouTube Link Search Tool")
        user_input = input("Enter artist and track name (Artist,TrackName) or Spotify link (or 'quit' to exit): ")

        if user_input.lower() == 'quit':
            break

        sp = Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

        if "spotify.com" in user_input:
            # User entered a Spotify link
            if "track/" in user_input:
                track_id = user_input.split("track/")[-1].split("?")[0]
                track_info = sp.track(track_id)
                artist = track_info['artists'][0]['name']
                track_name = track_info['name']
            else:
                print("Invalid Spotify link.")
                continue
        else:
            # User entered Artist,TrackName
            try:
                artist, track_name = user_input.split(",")
            except ValueError:
                print("Invalid input format. Please use 'Artist,TrackName' or a Spotify link.")
                continue

        youtube_link = get_youtube_link(artist, track_name)

        if youtube_link != "No results found on YouTube." and youtube_link != "No results found on Spotify.":
            print(f"YouTube Link: {youtube_link}")
            print("")
            print("")
        else:
            print(youtube_link)

if __name__ == "__main__":
    main()
