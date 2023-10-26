# sp.py - Spotify Link to YouTube // ArtistName,Song Name to YouTube

This Python program allows users to convert Spotify track information into YouTube links. It also allows for Artist + Song Name combinations to output youtube video links.

## Usage:

1. Make sure you have Python installed on your system.
2. Clone or download this repository.
3. pip install -r requirements.txt

## Running the Program:

1. Navigate to the directory containing the Python script.
2. Run the script using the following command:

python sp.py

3. The program will prompt you for the Spotify Client ID and Client Secret the first time you run it. These values will be saved for future runs in `client_id.txt` and `client_secret.txt`.



## Interacting with the Program:

You can interact with the program in two ways:

1. Enter Artist and Track Name: Type the artist and track name in the format `Artist,TrackName` and press Enter. The program will search for the YouTube link associated with that track.

2. Enter Spotify Link: If you provide a Spotify track link (e.g., `https://open.spotify.com/track/xxxxxxxxxxxxxxxxxxx`), the program will extract the track information and search for the corresponding YouTube link.

![Spotify to YouTube Link Converter](https://i.imgur.com/GqCPCXE.png)


## Exiting the Program:

To exit the program, type `quit` and press Enter.

## Requirements:

- Python 3.x
- Libraries: spotipy, youtube-search-python

## Files:

- lz.py: The main Python script.
- client_id.txt: Stores the Spotify Client ID.
- client_secret.txt: Stores the Spotify Client Secret.

## Notes:

- If `client_id.txt` and `client_secret.txt` are not found, the program will prompt you to enter these values.

How to get the spotify client id and secret:
- Go to the Spotify Developer Dashboard. (https://developer.spotify.com/dashboard)
- Log in with your Spotify account or create one if you don't have one.
- Click on "Create an App" and fill in the necessary information. You can name it anything you like.
- Once you've created the app, you'll see your client_id and client_secret on the app's dashboard.

## Dependencies:

- Spotipy: A lightweight Python library for the Spotify Web API.
- youtube-search-python: A Python library to search for YouTube videos.

## License:

This project is licensed under the MIT License - see the LICENSE file for details.


## Support:

Feel like this has been useful? Donate toward my latest projects. https://www.poof.io/tip/@davidinfosec