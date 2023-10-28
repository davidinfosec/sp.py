import sys
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch
import csv
import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import requests

# Initialize Spotify Client ID and Secret
try:
    with open('./client_id.txt', 'r') as file:
        SPOTIPY_CLIENT_ID = file.read().strip()
except FileNotFoundError:
    SPOTIPY_CLIENT_ID = input("Enter your Spotify Client ID: ")
    with open('./client_id.txt', 'w') as file:
        file.write(SPOTIPY_CLIENT_ID)

try:
    with open('./client_secret.txt', 'r') as file:
        SPOTIPY_CLIENT_SECRET = file.read().strip()
except FileNotFoundError:
    SPOTIPY_CLIENT_SECRET = input("Enter your Spotify Client Secret: ")
    with open('./client_secret.txt', 'w') as file:
        file.write(SPOTIPY_CLIENT_SECRET)

# Define a cache for API requests
api_cache = {}

# Define a list to store recent searches
recent_searches = []

# Define a subdirectory for CSV files
current_date = datetime.datetime.now().strftime("%Y-%m")
subdirectory = f"sp-{current_date}"

if not os.path.exists(subdirectory):
    os.makedirs(subdirectory)

csv_file = f"{subdirectory}/sp-py-{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"

# Initialize CSV with headers if it doesn't exist
def initialize_csv(csv_file):
    if not os.path.exists(csv_file):
        headers = ["Type", "Playlist Name", "Search Term", "Spotify Link", "YouTube Link"]
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

# Define a function to get YouTube link and song info with caching
def get_youtube_link_cached(artist, track_name):
    query = f"{artist} {track_name} official video"
    if query in api_cache:
        return api_cache[query]

    youtube_results = YoutubeSearch(query, max_results=1).to_dict()
    if youtube_results:
        youtube_link = f"https://www.youtube.com/watch?v={youtube_results[0]['id']}"
        result = (youtube_link, f"Song name: {artist} - {track_name}")
    else:
        result = ("No results found on YouTube.",)
    api_cache[query] = result
    return result

# Define a function to get Spotify link
def get_spotify_link(artist, track_name):
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    query = f"artist:{artist} track:{track_name}"
    results = sp.search(q=query, type='track', limit=1)

    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['id']
        spotify_link = f"https://open.spotify.com/track/{track_id}"
        return spotify_link
    else:
        return "No results found on Spotify."

# Define a function to export recent searches to CSV
def export_recent_searches(csv_file):
    if recent_searches:
        if not os.path.exists(csv_file):
            initialize_csv(csv_file)
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for entry in recent_searches:
                writer.writerow(entry)
        print(f"Searches appended to {csv_file}")
        recent_searches.clear()

# Define a function to clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Define a function to process a track
def process_track(track, playlist_name):
    artist = track['track']['artists'][0]['name']
    track_name = track['track']['name']

    youtube_link, song_info = get_youtube_link_cached(artist, track_name)

    if youtube_link != "No results found on YouTube." and youtube_link != "No results found on Spotify.":
        print()
        print()
        print()
        print(f"YouTube Link: {youtube_link}")
        spotify_link = get_spotify_link(artist, track_name)
        if spotify_link:
            print(f"Spotify Link: {spotify_link}")
        print(song_info)
        print("\n\n")
        recent_searches.append(["Single", playlist_name, f"{artist} - {track_name}", spotify_link, youtube_link])
        export_recent_searches(csv_file)
        send_message_to_webhook(webhook_url, f"YouTube Link: {youtube_link}\n{song_info}\n\n")
    else:
        print(youtube_link)

# Define a function to process a playlist for bulk search
def process_playlist(playlist_link, playlist_name):
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    # Extract playlist ID from the link
    playlist_id = playlist_link.split("playlist/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_id)

    total_tracks = results['total']

    if total_tracks > 0:
        with ThreadPoolExecutor() as executor:
            list(tqdm(executor.map(process_track, results['items'], [playlist_name]*total_tracks), total=total_tracks, desc=f"Processing tracks in playlist '{playlist_name}'", unit="track"))
    else:
        print(f"No tracks found in playlist '{playlist_name}'.")

# Define a function to manage webhook settings
def manage_webhook():
    global webhook_url
    use_webhook = input("Do you want to use a webhook for notifications? (yes/no): ").lower()
    if use_webhook == 'yes':
        webhook_url = input("Enter your Discord webhook URL: ")
        with open('./webhook_url.txt', 'w') as file:
            file.write(webhook_url)
    elif use_webhook == 'no':
        webhook_url = None
        if os.path.exists('./webhook_url.txt'):
            os.remove('./webhook_url.txt')

# Define a function to send a message to the webhook
def send_message_to_webhook(webhook_url, message):
    if webhook_url is not None:
        payload = {'content': message}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response status codes


# Define the main function
def main():
    global webhook_url
    sp = Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))
    
    if not os.path.exists(csv_file):
        initialize_csv(csv_file)

    manage_webhook()  # Ask user about webhook preference

    while True:
        clear_screen()
        print("Spotify to YouTube / YouTube Link Search Tool")
        print(r'''
   ___ _ __   _ __  _   _ 
  / __| '_ \ | '_ \| | | |
  \__ \ |_) || |_) | |_| |
  |___/ .__(_) .__/ \__, |
      | |    | |     __/ |
      |_|    |_|    |___/ 
        ''')
        user_input = input("Enter artist and track name (Artist,TrackName), Spotify link, 'cls' to clear screen, '--bulk PlaylistLink PlaylistName' to process a playlist, or 'quit' to exit (c to cancel): ")

        if user_input.lower() == 'quit':
            break

        if user_input.lower() == 'cls':
            clear_screen()
            continue

        if user_input.lower() == 'c':
            print("Process cancelled.")
            break

        if user_input.startswith('--bulk'):
            args = user_input.split(maxsplit=2)
            if len(args) == 3:
                _, link, playlist_name = args
                if link.startswith("https://open.spotify.com/album/"):
                    process_album(link)
                else:
                    process_playlist(link, playlist_name)
            else:
                print("Invalid input format. Please use '--bulk Link PlaylistName' or '--bulk-album AlbumLink'.")
            continue

        spotify_link = ""
        if "spotify.com" in user_input:
            if "track/" in user_input:
                track_id = user_input.split("track/")[-1].split("?")[0]
                spotify_link = f"https://open.spotify.com/track/{track_id}"
                track_info = sp.track(track_id)
                artist = track_info['artists'][0]['name']
                track_name = track_info['name']
            elif "album/" in user_input:
                album_id = user_input.split("album/")[-1].split("?")[0]
                results = sp.album_tracks(album_id)
                total_tracks = len(results['items']) if 'items' in results else 0

                if total_tracks > 0:
                    process_album(user_input)
                else:
                    print("No tracks found in the album.")
                continue
            else:
                print("Invalid Spotify link.")
                continue
        else:
            try:
                artist, track_name = user_input.split(",")
            except ValueError:
                print("Invalid input format. Please use 'Artist,TrackName' or a Spotify link.")
                continue

        youtube_link, song_info = get_youtube_link_cached(artist, track_name)

        if youtube_link != "No results found on YouTube." and youtube_link != "No results found on Spotify.":
            print()
            print()
            print()
            print(f"YouTube Link: {youtube_link}")
            if spotify_link:
                print(f"Spotify Link: {spotify_link}")
            print(song_info)
            print("\n\n")
            recent_searches.append(["Single", "N/A", f"{artist} - {track_name}", spotify_link, youtube_link])
            export_recent_searches(csv_file)
            send_message_to_webhook(webhook_url, f"YouTube Link: {youtube_link}\n{song_info}\n\n")
        else:
            print(youtube_link)

        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
