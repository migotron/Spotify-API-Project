import os
import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pycountry

# Set up client credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Set database name
DATABASE_NAME = "song_data.db"

# Check if contacts.db exists
if not os.path.exists(DATABASE_NAME):
    # Create database file and table
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS songs
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              artist_name TEXT,
              track_name TEXT,
              danceability REAL,
              energy REAL,
              key INTEGER,
              loudness REAL,
              mode INTEGER,
              speechiness REAL,
              acousticness REAL,
              instrumentalness REAL,
              liveness REAL,
              valence REAL,
              tempo REAL,
              popularity INTEGER,
              duration_ms INTEGER,
              num_markets INTEGER,
              album_name TEXT,
              album_type TEXT,
              release_date TEXT,
              explicit INTEGER,
              track_number INTEGER,
              release_type TEXT,
              isrc TEXT,
              href TEXT,
              external_url TEXT,
              external_ids TEXT)''')
    c.close()
    
# Connect to database
conn = sqlite3.connect(DATABASE_NAME)
c = conn.cursor()


# Prompt the user for an artist name
artist_name = input('Enter the name of an artist: ')

# Search for the artist
results = sp.search(q='artist:' + artist_name, type='artist')
items = results['artists']['items']

if len(items) > 0:
    # Retrieve the artist's Spotify ID
    artist = items[0]
    artist_id = artist['id']
    
    results2 = sp.search(q=artist_name, limit=1)
    artist_uri = results2['tracks']['items'][0]['artists'][0]['uri']

    album_ids = []
    albums = sp.artist_albums(artist_uri, album_type='album,single', limit=50)['items']
    for album in albums:
        album_ids.append(album['id'])

    top_countries = set()
    for album_id in album_ids:
        album = sp.album(album_id)
        top_countries.update(album['available_markets'])

    country_names = []
    for code in top_countries:
        country = pycountry.countries.get(alpha_2=code)
        if country is not None:
            country_names.append(country.name)

    top_countries = list(set(country_names))
    
    if len(top_countries) == 0:
        print(f"Sorry, we couldn't find any countries where {artist_name}'s music is available.")
    else:
        print(f"Here are the top countries where {artist_name}'s music is available:")
        for i, country_name in enumerate(top_countries, 1):
            print(f"{i}. {country_name}")

    # Retrieve the artist's top 10 tracks
    top_tracks = sp.artist_top_tracks(artist_id=artist_id)
    print('Top Tracks for ' + artist_name + ':')
    for i, track in enumerate(top_tracks['tracks']):
        # Get the audio features for the track
        audio_features = sp.audio_features(track['id'])[0]
        
        # Get the track popularity
        track_info = sp.track(track['id'])
        popularity = track_info['popularity']
        num_streams = track_info['popularity'] * 1000000
        
        # Insert the data into the database if it doesn't already exist
        c.execute('''SELECT id FROM songs WHERE artist_name=? AND track_name=?''',
                  (artist_name, track['name']))
        data = c.fetchone()
        if data is None:
            c.execute('''INSERT INTO songs (artist_name, track_name, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, popularity, duration_ms, num_markets, album_name, album_type, release_date, explicit, track_number, release_type, isrc, href, external_url, external_ids) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (artist_name, track['name'], audio_features['danceability'], audio_features['energy'], audio_features['key'], audio_features['loudness'], audio_features['mode'], audio_features['speechiness'], audio_features['acousticness'], audio_features['instrumentalness'], audio_features['liveness'], audio_features['valence'], audio_features['tempo'], popularity, track_info['duration_ms'], len(track_info['album']['available_markets']), track_info['album']['name'], track_info['album']['album_type'], track_info['album']['release_date'], track_info['explicit'], track_info['track_number'], track_info['type'], track_info['external_ids']['isrc'], track_info['href'], track_info['external_urls']['spotify'], str(track_info['external_ids'])))
            conn.commit()
        
        # Print the track name and audio features
        print(str(i+1) + '. ' + track['name'])
        print('   - danceability: ' + str(audio_features['danceability']))
        print('   - energy: ' + str(audio_features['energy']))
        print('   - key: ' + str(audio_features['key']))
        print('   - loudness: ' + str(audio_features['loudness']))
        print('   - mode: ' + str(audio_features['mode']))
        print('   - speechiness: ' + str(audio_features['speechiness']))
        print('   - acousticness: ' + str(audio_features['acousticness']))
        print('   - instrumentalness: ' + str(audio_features['instrumentalness']))
        print('   - liveness: ' + str(audio_features['liveness']))
        print('   - valence: ' + str(audio_features['valence']))
        print('   - tempo: ' + str(audio_features['tempo']))
        print('   - popularity: ' + str(popularity))
        print('   - num_streams: ' + str(num_streams))
        print('   - explicit: ' + str(track_info['explicit']))
        print('   - track number: ' + str(track_info['track_number']))
        print('   - release type: ' + track_info['type'])
        print('   - ISRC: ' + track_info['external_ids']['isrc'])
        print('   - href: ' + track_info['href'])
        print('   - external URL: ' + track_info['external_urls']['spotify'])
        print('   - external IDs: ' + str(track_info['external_ids']))
else:
    print('No artist found with the name ' + artist_name)

# Close the database connection
conn.close()
