import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from .secrets import *

client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_album_tracks(j_file):
    uri = []
    tracks = []
    duration = []
    album = []
    artist = []
    played_at = []
    
    for track in j_file['items']:
        uri.append(track['track']['uri'])
        tracks.append(track['track']['name'])
        duration.append(track['track']['duration_ms'])
        album.append(track['track']['album']['name'])
        artist.append(track['track']['artists'][0]['name'])
        played_at.append(track['played_at'])

    df2 = pd.DataFrame({
    'uri':uri,
    'track':tracks,
    'duration_ms':duration,
    'album':album,
    'artist':artist,
    'played_at': played_at})

    return df2

#insert output dataframe from the get_album_tracks function
def get_track_info(df):
    danceability = []
    energy = []
    key = []
    loudness = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []

    for i in df['uri']:
        for x in sp.audio_features(tracks=[i]):
            danceability.append(x['danceability'])
            energy.append(x['energy'])
            key.append(x['key'])
            loudness.append(x['loudness'])
            speechiness.append(x['speechiness'])
            acousticness.append(x['acousticness'])
            instrumentalness.append(x['instrumentalness'])
            liveness.append(x['liveness'])
            valence.append(x['valence'])
            tempo.append(x['tempo'])
            
    df2 = pd.DataFrame({
    'danceability':danceability,
    'energy':energy,
    'key':key,
    'loudness':loudness,
    'speechiness':speechiness,
    'acousticness':acousticness,
    'instrumentalness':instrumentalness,
    'liveness':liveness,
    'valence':valence,
    'tempo':tempo})
    
    return df2

def merge_frames(df1, df2):
    df3 = df1.merge(df2, left_index= True, right_index= True)
    return df3
