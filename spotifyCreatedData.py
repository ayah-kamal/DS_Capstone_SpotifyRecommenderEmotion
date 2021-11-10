import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from lyricsScraping import *

clientID = "6b3d7d7b52324366a650f2d43388ffe2"
clientSecret = "c2666658cce64c1bae9c371eccca0a9c"

client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Spotify generated playlist according to certain moods
sad_songs_playlist = "37i9dQZF1DX7qK8ma5wgG1"
sad_songs_playlist_1 = "37i9dQZF1DWX83CujKHHOn"
sad_songs_playlist_2 = "38BAFacbwA5kGf7iqcW7Wj"
happy_songs_playlist = "37i9dQZF1DXdPec7aLTmlC"
happy_songs_playlist_1 = "37i9dQZF1DX9XIFQuFvzM4"
happy_songs_playlist_2 = "37i9dQZF1DX3rxVfibe1L0"
energy_songs_playlist = "37i9dQZF1DX0vHZ8elq0UK"
energy_songs_playlist_1 = "37i9dQZF1DX8hY56Fq3fM0"
calm_songs_playlist = "37i9dQZF1DWWpO97CaFM3p"
calm_songs_playlist_1 = "37i9dQZF1DXaXDsfv6nvZ5"
calm_songs_playlist_2 = "11q1sTpWABVhGmIBcfDLtt"
angry_songs_playlist = "6ft4ijUITtTeVC0dUCDdvH"
angry_songs_playlist_1 ="3ZzI0mlze2kT37u9lQwUcO"
angry_songs_playlist_2 = "0s5O323LN8dpV81h33OoZQ"


def call_playlist(creator, playlist_id):
    
    playlist_features_list = ["artist","album","track", "track_id",'danceability',
 'energy',
 'key',
 'loudness',
 'speechiness',
 'acousticness',
 'instrumentalness',
 'liveness',
 'valence',
 'tempo', "duration_ms","time_signature"]

    playlist_df = pd.DataFrame(columns = playlist_features_list)

    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    for track in playlist:
        # Create empty dict
        playlist_features = {}
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track"] = track["track"]["name"]
        playlist_features["duration_ms"] = track['track']['duration_ms']
        playlist_features["track_id"] = track["track"]["id"]
        
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]
        
        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        
    return playlist_df

sad_songs_df = call_playlist("spotify",sad_songs_playlist)
happy_songs_df = call_playlist("spotify",happy_songs_playlist)
energy_songs_df = call_playlist("spotify",energy_songs_playlist)
calm_songs_df = call_playlist("spotify",calm_songs_playlist)

sad_songs_df1 = call_playlist("spotify",sad_songs_playlist_1)
happy_songs_df1 = call_playlist("spotify",happy_songs_playlist_1)
happy_songs_df2 = call_playlist("spotify",happy_songs_playlist_2)
energy_songs_df1 = call_playlist("spotify",energy_songs_playlist_1)
calm_songs_df1 = call_playlist("spotify",calm_songs_playlist_1)

calm_songs_df2 = call_playlist("spotify",calm_songs_playlist_2)
angry_songs_df = call_playlist("spotify",angry_songs_playlist)
angry_songs_df1 = call_playlist("spotify",angry_songs_playlist_1)
angry_songs_df2 = call_playlist("spotify",angry_songs_playlist_2)
sad_songs_df2 = call_playlist("spotify",sad_songs_playlist_2)

sad_songs_df['mood'] = 'Sad'
sad_songs_df1['mood'] = 'Sad'
sad_songs_df2['mood'] = 'Sad'
happy_songs_df['mood'] = 'Happy'
happy_songs_df1['mood'] = 'Happy'
happy_songs_df2['mood'] = 'Happy'
energy_songs_df['mood'] = 'Energy'
energy_songs_df1['mood'] = 'Energy'
calm_songs_df['mood'] = 'Calm'
calm_songs_df1['mood'] = 'Calm'
calm_songs_df2['mood'] = 'Calm'
angry_songs_df['mood'] = 'Angry'
angry_songs_df1['mood'] = 'Angry'
angry_songs_df2['mood'] = 'Angry'

# exporting dataframes as csv to scrape lyrics
# worked in smaller batches to avoid getting blocked
'''
sad_songs_df.to_csv(r".\sad_mood_dataset.csv", index = False)
sad_songs_df1.to_csv(r".\sad_mood_1_dataset.csv", index = False)
sad_songs_df2.to_csv(r".\sad_mood_2_dataset.csv", index = False)

happy_songs_df.to_csv(r".\happy_mood_dataset.csv", index = False)
happy_songs_df1.to_csv(r".\happy_mood_1_dataset.csv", index = False)
happy_songs_df2.to_csv(r".\happy_mood_2_dataset.csv", index = False)

energy_songs_df.to_csv(r".\energy_mood_dataset.csv", index = False)
energy_songs_df1.to_csv(r".\energy_mood_1_dataset.csv", index = False)

calm_songs_df.to_csv(r".\calm_mood_dataset.csv", index = False)
calm_songs_df1.to_csv(r".\calm_mood_1_dataset.csv", index = False)
calm_songs_df2.to_csv(r".\calm_mood_2_dataset.csv", index = False)

angry_songs_df.to_csv(r".\angry_mood_dataset.csv", index = False)
angry_songs_df1.to_csv(r".\angry_mood_1_dataset.csv", index = False)
angry_songs_df2.to_csv(r".\angry_mood_1_dataset.csv", index = False)
'''

# Reading in indivisual mood playlists after lyrics are scraped
sad_songs_df= pd.read_csv("indiv_mood_playlists/sad_mood_dataset.csv")
sad_songs_df1= pd.read_csv("indiv_mood_playlists/sad_mood_1_dataset.csv")
sad_songs_df2= pd.read_csv("indiv_mood_playlists/sad_mood_2_dataset.csv")

happy_songs_df= pd.read_csv("indiv_mood_playlists/happy_mood_dataset.csv")
happy_songs_df1= pd.read_csv("indiv_mood_playlists/happy_mood_1_dataset.csv")
happy_songs_df2= pd.read_csv("indiv_mood_playlists/happy_mood_2_dataset.csv")

energy_songs_df= pd.read_csv("indiv_mood_playlists/energy_mood_dataset.csv")
energy_songs_df1= pd.read_csv("indiv_mood_playlists/energy_mood_1_dataset.csv")

calm_songs_df= pd.read_csv("indiv_mood_playlists/calm_mood_dataset.csv")
calm_songs_df1= pd.read_csv("indiv_mood_playlists/calm_mood_1_dataset.csv")
calm_songs_df2= pd.read_csv("indiv_mood_playlists/calm_mood_2_dataset.csv")

angry_songs_df= pd.read_csv("indiv_mood_playlists/angry_mood_dataset.csv")
angry_songs_df1= pd.read_csv("indiv_mood_playlists/angry_mood_1_dataset.csv")
angry_songs_df2= pd.read_csv("indiv_mood_playlists/angry_mood_1_dataset.csv")


sad_df = pd.concat([sad_songs_df, sad_songs_df1, sad_songs_df2])
happy_df = pd.concat([happy_songs_df, happy_songs_df1, happy_songs_df2])
energy_df = pd.concat([energy_songs_df, energy_songs_df1])
calm_df = pd.concat([calm_songs_df, calm_songs_df1, calm_songs_df2])
angry_df = pd.concat([angry_songs_df, angry_songs_df1, angry_songs_df2])

def concatFrames(df1, df2, df3, df4, df5):
    df = pd.concat([df1,df2,df3,df4,df5], 
    ignore_index= True)
    return df

mood_data=concatFrames(sad_df, happy_df, energy_df, calm_df, angry_df)

mood_data_df = mood_data.sort_values(by = 'track')
mood_data_df = mood_data_df.reset_index(drop = True)

mood_data_df.to_csv(r".\spotify_mood_dataset.csv", index = False)
mood_data_df
