# Spotify Song Data

This repository contains a Python script that uses the [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/) library to interact with the [Spotify Web API](https://developer.spotify.com/documentation/web-api/). The script retrieves information about an artist's top tracks and stores it in a SQLite database.

## Prerequisites

Before running the script, you'll need to have the following installed:
- **Python 3**: The script is written in Python 3 and requires it to be installed on your system.
- **Spotipy**: This is a Python library for the Spotify Web API. It provides a simple interface for interacting with the API and retrieving data.
- **pycountry**: This is a Python library that provides ISO country, subdivision, language, currency and script definitions and their translations.

You'll also need to set up a Spotify Developer account and register an application to obtain a `client_id` and `client_secret`. These values should be set as environment variables named `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`, respectively.

## Installation

To install the required libraries, you can use `pip` by running the following command:

```
pip install spotipy pycountry
```

## Usage

To run the script, navigate to the directory containing the script and run the following command:

```
python3 spotify_api.py
```

Replace `spotify_api.py` with the name of the script file.

The script will prompt you to enter the name of an artist. After entering the artist's name, the script will search for the artist on Spotify and retrieve their top tracks. The track information will be stored in a SQLite database named `song_data.db`.

The database contains a table named `songs` with columns for various track attributes such as `artist_name`, `track_name`, `danceability`, `energy`, etc. The script will insert data into this table for each of the artist's top tracks.

### Here's a brief explanation of what each part of the code does:

1. The first few lines of the code import the necessary libraries: `os`, `sqlite3`, `spotipy`, `SpotifyClientCredentials` from `spotipy.oauth2`, and `pycountry`.
2. The next few lines set up the client credentials for accessing the Spotify Web API using the `SpotifyClientCredentials` class from the `spotipy.oauth2` module. The `client_id` and `client_secret` are retrieved from environment variables and passed to the `SpotifyClientCredentials` constructor. A `spotipy.Spotify` object is then created using the `client_credentials_manager` parameter.
3. The database name is set to `"song_data.db"`.
4. The code checks if the database file exists. If it doesn't, a new SQLite database file is created and a table named `songs` is created in the database with columns for various track attributes.
5. A connection to the database is established and a cursor object is created.
6. The user is prompted to enter the name of an artist.
7. The code searches for the artist on Spotify using the `search` method of the `spotipy.Spotify` object and retrieves the artist's Spotify ID.
8. The code retrieves information about the artist's albums and top tracks using various methods of the `spotipy.Spotify` object such as `artist_albums`, `album`, and `artist_top_tracks`.
9. For each of the artist's top tracks, the code retrieves audio features and popularity information using methods such as `audio_features` and `track`.
10. The track information is inserted into the `songs` table in the database if it doesn't already exist.
11. The track name and audio features are printed to the console.
12. Finally, the database connection is closed.

## Contributing

Contributions are welcome! If you have any ideas for new features or improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
