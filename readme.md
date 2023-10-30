## sp.py - Spotify Link to YouTube / ArtistName,SongName to YouTube

This Python program allows users to convert Spotify track information into YouTube links. It also allows for Artist + Song Name combinations to output youtube video links.

Transparency: Most of this app was created with AI assistance, as I seek to find solutions to my problems in creative ways. After finding use of such a tool, it is only fair to share it with others who may benefit in the same way.

## Usage:

1. Make sure you have Python installed on your system.
2. Clone or download this repository.
3. pip install -r requirements.txt

## Running the Program:

1. Navigate to the directory containing the Python script.
2. Run the script using the following command:

python sp.py

3. The program will prompt you for the Spotify Client ID and Client Secret the first time you run it. These values will be saved for future runs in `client_id.txt` and `client_secret.txt`.

How to get the spotify client id and secret:
- Go to the Spotify Developer Dashboard. (https://developer.spotify.com/dashboard)
- Log in with your Spotify account or create one if you don't have one.
- Click on "Create an App" and fill in the necessary information. You can name it anything you like.
- Once you've created the app, you'll see your client_id and client_secret on the app's dashboard.

## Interacting with the Program:

You can interact with the program in a few ways:

1. Enter Artist and Track Name: Type the artist and track name in the format `Artist,TrackName` and press Enter. The program will search for the YouTube link associated with that track.

2. Enter Spotify Link: If you provide a Spotify track link (e.g., `https://open.spotify.com/track/xxxxxxxxxxxxxxxxxxx`), the program will extract the track information and search for the corresponding YouTube link.

3. You can also use the ``--bulk`` flag to query a playlist for youtube links.
      EX. ``--bulk [SpotifyPlaylistLink] [NameOrDescriptor]``

4. Optional Discord Webhook support: simply specify a webhook URL when prompted. You will not be prompted again unless you delete your webhook_url.txt file, generated in the same directory as the program, or unless you specify a different webhook with --webhook

The playlist processing is a bit buggy with its current implementation and will only process up to 100 songs reliably. Keep your queries below 100 songs if you want to guarantee a fully processed playlist. May also crash the program. Bulk is buggy :(

Output will be generated to a .csv file dated and located under the sp-YYYY-MM folder

![Spotify to YouTube Link Converter](https://i.imgur.com/GqCPCXE.png)


## Exiting the Program:

To exit the program, type `quit` and press Enter.

## Requirements:

- Python 3.x
- Libraries: spotipy, youtube-search-python

## Files:

- sp.py: The main Python script.
- client_id.txt: Stores the Spotify Client ID.
- client_secret.txt: Stores the Spotify Client Secret.

## Dependencies:

- Spotipy: A lightweight Python library for the Spotify Web API.
- youtube-search-python: A Python library to search for YouTube videos.

## Support:

Feel like this has been useful? Donate toward my latest projects. https://www.poof.io/tip/@davidinfosec
