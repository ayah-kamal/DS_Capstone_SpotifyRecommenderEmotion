import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from lyricsScraping import *
from secrets import *

client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Spotify generated playlist according to certain moods
sad_songs_playlist = "37i9dQZF1DX7qK8ma5wgG1"
sad_songs_playlist_1 = "37i9dQZF1DWX83CujKHHOn"
sad_songs_playlist_2 = "38BAFacbwA5kGf7iqcW7Wj"
sad_songs_playlist_3 = "70VaOHyjpsWcmA4gxosExZ"
sad_songs_playlist_4 = "0tLAnPmh7VpPKBu8v6pZXd"
sad_songs_playlist_5 = "53NEfJTEt86ytgk5SaqMjZ"
happy_songs_playlist = "37i9dQZF1DXdPec7aLTmlC"
happy_songs_playlist_1 = "37i9dQZF1DX9XIFQuFvzM4"
happy_songs_playlist_2 = "37i9dQZF1DX3rxVfibe1L0"
happy_songs_playlist_3 = "5yI34GDYLxUxfSrpshdNVE"
happy_songs_playlist_4 = "0RH319xCjeU8VyTSqCF6M4"
happy_songs_playlist_5 = "6kTimgeEnsD7JsEQlvCBoS"
energy_songs_playlist = "37i9dQZF1DX0vHZ8elq0UK"
energy_songs_playlist_1 = "37i9dQZF1DX8hY56Fq3fM0"
energy_songs_playlist_2 ="2lmcuXNkjYOoQeXvwqvvFT"
energy_songs_playlist_3 ="5usLXHq0ZrH37KkBG4xHTN"
energy_songs_playlist_4 ="6kIo3hkGUX6WyfthHfGDOm"
energy_songs_playlist_5 ="1LWAdcRpaRcFqX3g4e2dGl"
calm_songs_playlist = "37i9dQZF1DWWpO97CaFM3p"
calm_songs_playlist_1 = "37i9dQZF1DXaXDsfv6nvZ5"
calm_songs_playlist_2 = "11q1sTpWABVhGmIBcfDLtt"
calm_songs_playlist_3 = "167zIkUCJ45vTj0exwQHxK"
calm_songs_playlist_4 = "0nINy1bfIZYU6nrHKKXbBV"
calm_songs_playlist_5 = "5bjuQJ93MM2Qi2olxIIgWX"
angry_songs_playlist = "6ft4ijUITtTeVC0dUCDdvH"
angry_songs_playlist_1 ="3ZzI0mlze2kT37u9lQwUcO"
angry_songs_playlist_2 = "0s5O323LN8dpV81h33OoZQ"
angry_songs_playlist_3 = "5bWn8XcgI3hv2vpWjNq8la"
angry_songs_playlist_4 = "3aBeWOxyVcFupF8sKMm2k7"
angry_songs_playlist_5 ="6aB3XCffMGOj7rDL6jqGtl"

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
sad_songs_df1 = call_playlist("spotify",sad_songs_playlist_1)
sad_songs_df2 = call_playlist("spotify",sad_songs_playlist_2)
sad_songs_df3 = call_playlist("spotify",sad_songs_playlist_3)
sad_songs_df4 = call_playlist("spotify",sad_songs_playlist_4)
sad_songs_df5 = call_playlist("spotify",sad_songs_playlist_5)

happy_songs_df = call_playlist("spotify",happy_songs_playlist)
happy_songs_df1 = call_playlist("spotify",happy_songs_playlist_1)
happy_songs_df2 = call_playlist("spotify",happy_songs_playlist_2)
happy_songs_df3 = call_playlist("spotify",happy_songs_playlist_3)
happy_songs_df4 = call_playlist("spotify",happy_songs_playlist_4)
happy_songs_df5 = call_playlist("spotify",happy_songs_playlist_5)

energy_songs_df = call_playlist("spotify",energy_songs_playlist)
energy_songs_df1 = call_playlist("spotify",energy_songs_playlist_1)
energy_songs_df2 = call_playlist("spotify",energy_songs_playlist_2)
energy_songs_df3 = call_playlist("spotify",energy_songs_playlist_3)
energy_songs_df4 = call_playlist("spotify",energy_songs_playlist_4)
energy_songs_df5 = call_playlist("spotify",energy_songs_playlist_5)

calm_songs_df = call_playlist("spotify",calm_songs_playlist)
calm_songs_df1 = call_playlist("spotify",calm_songs_playlist_1)
calm_songs_df2 = call_playlist("spotify",calm_songs_playlist_2)
calm_songs_df3 = call_playlist("spotify",calm_songs_playlist_3)
calm_songs_df4 = call_playlist("spotify",calm_songs_playlist_4)
calm_songs_df5 = call_playlist("spotify",calm_songs_playlist_5)


angry_songs_df = call_playlist("spotify",angry_songs_playlist)
angry_songs_df1 = call_playlist("spotify",angry_songs_playlist_1)
angry_songs_df2 = call_playlist("spotify",angry_songs_playlist_2)
angry_songs_df3 = call_playlist("spotify",angry_songs_playlist_3)
angry_songs_df4 = call_playlist("spotify",angry_songs_playlist_4)
angry_songs_df5 = call_playlist("spotify",angry_songs_playlist_5)


sad_songs_df['mood'] = 'Sad'
sad_songs_df1['mood'] = 'Sad'
sad_songs_df2['mood'] = 'Sad'
sad_songs_df3['mood'] = 'Sad'
sad_songs_df4['mood'] = 'Sad'
sad_songs_df5['mood'] = 'Sad'
happy_songs_df['mood'] = 'Happy'
happy_songs_df1['mood'] = 'Happy'
happy_songs_df2['mood'] = 'Happy'
happy_songs_df3['mood'] = 'Happy'
happy_songs_df4['mood'] = 'Happy'
happy_songs_df5['mood'] = 'Happy'
energy_songs_df['mood'] = 'Energy'
energy_songs_df1['mood'] = 'Energy'
energy_songs_df2['mood'] = 'Energy'
energy_songs_df3['mood'] = 'Energy'
energy_songs_df4['mood'] = 'Energy'
energy_songs_df5['mood'] = 'Energy'
calm_songs_df['mood'] = 'Calm'
calm_songs_df1['mood'] = 'Calm'
calm_songs_df2['mood'] = 'Calm'
calm_songs_df3['mood'] = 'Calm'
calm_songs_df4['mood'] = 'Calm'
calm_songs_df5['mood'] = 'Calm'
angry_songs_df['mood'] = 'Angry'
angry_songs_df1['mood'] = 'Angry'
angry_songs_df2['mood'] = 'Angry'
angry_songs_df3['mood'] = 'Angry'
angry_songs_df4['mood'] = 'Angry'
angry_songs_df5['mood'] = 'Angry'

# exporting dataframes as csv to scrape lyrics
# worked in smaller batches to avoid getting blocked
'''

sad_songs_df.to_csv(r".\sad_mood_dataset.csv", index = False)
sad_songs_df1.to_csv(r".\sad_mood_1_dataset.csv", index = False)
sad_songs_df2.to_csv(r".\sad_mood_2_dataset.csv", index = False)
sad_songs_df3.to_csv(r".\sad_mood_3_dataset.csv", index = False)
sad_songs_df4.to_csv(r".\sad_mood_4_dataset.csv", index = False)
sad_songs_df5.to_csv(r".\sad_mood_5_dataset.csv", index = False)

happy_songs_df.to_csv(r".\happy_mood_dataset.csv", index = False)
happy_songs_df1.to_csv(r".\happy_mood_1_dataset.csv", index = False)
happy_songs_df2.to_csv(r".\happy_mood_2_dataset.csv", index = False)
happy_songs_df3.to_csv(r".\happy_mood_3_dataset.csv", index = False)
happy_songs_df4.to_csv(r".\happy_mood_4_dataset.csv", index = False)
happy_songs_df5.to_csv(r".\happy_mood_5_dataset.csv", index = False)

energy_songs_df.to_csv(r".\energy_mood_dataset.csv", index = False)
energy_songs_df1.to_csv(r".\energy_mood_1_dataset.csv", index = False)
energy_songs_df2.to_csv(r".\energy_mood_2_dataset.csv", index = False)
energy_songs_df3.to_csv(r".\energy_mood_3_dataset.csv", index = False)
energy_songs_df4.to_csv(r".\energy_mood_4_dataset.csv", index = False)
energy_songs_df5.to_csv(r".\energy_mood_5_dataset.csv", index = False)

calm_songs_df.to_csv(r".\calm_mood_dataset.csv", index = False)
calm_songs_df1.to_csv(r".\calm_mood_1_dataset.csv", index = False)
calm_songs_df2.to_csv(r".\calm_mood_2_dataset.csv", index = False)
calm_songs_df3.to_csv(r".\calm_mood_3_dataset.csv", index = False)
calm_songs_df4.to_csv(r".\calm_mood_4_dataset.csv", index = False)
calm_songs_df5.to_csv(r".\calm_mood_5_dataset.csv", index = False)

angry_songs_df.to_csv(r".\angry_mood_dataset.csv", index = False)
angry_songs_df1.to_csv(r".\angry_mood_1_dataset.csv", index = False)
angry_songs_df2.to_csv(r".\angry_mood_2_dataset.csv", index = False)
angry_songs_df3.to_csv(r".\angry_mood_3_dataset.csv", index = False)
angry_songs_df4.to_csv(r".\angry_mood_4_dataset.csv", index = False)
angry_songs_df5.to_csv(r".\angry_mood_5_dataset.csv", index = False)
'''

# Reading in individual mood playlists after lyrics are scraped
sad_songs_df= pd.read_csv("indiv_mood_playlists/sad_mood_dataset.csv")
sad_songs_df1= pd.read_csv("indiv_mood_playlists/sad_mood_1_dataset.csv")
sad_songs_df2= pd.read_csv("indiv_mood_playlists/sad_mood_2_dataset.csv")
sad_songs_df3= pd.read_csv("indiv_mood_playlists/sad_mood_3_dataset.csv")
sad_songs_df4= pd.read_csv("indiv_mood_playlists/sad_mood_4_dataset.csv")
sad_songs_df5= pd.read_csv("indiv_mood_playlists/sad_mood_5_dataset.csv")

happy_songs_df= pd.read_csv("indiv_mood_playlists/happy_mood_dataset.csv")
happy_songs_df1= pd.read_csv("indiv_mood_playlists/happy_mood_1_dataset.csv")
happy_songs_df2= pd.read_csv("indiv_mood_playlists/happy_mood_2_dataset.csv")
happy_songs_df3= pd.read_csv("indiv_mood_playlists/happy_mood_3_dataset.csv")
happy_songs_df4= pd.read_csv("indiv_mood_playlists/happy_mood_4_dataset.csv")
happy_songs_df5= pd.read_csv("indiv_mood_playlists/happy_mood_5_dataset.csv")

energy_songs_df= pd.read_csv("indiv_mood_playlists/energy_mood_dataset.csv")
energy_songs_df1= pd.read_csv("indiv_mood_playlists/energy_mood_1_dataset.csv")
energy_songs_df2= pd.read_csv("indiv_mood_playlists/energy_mood_2_dataset.csv")
energy_songs_df3= pd.read_csv("indiv_mood_playlists/energy_mood_3_dataset.csv")
energy_songs_df4 = pd.read_csv("indiv_mood_playlists/energy_mood_4_dataset.csv")
energy_songs_df5= pd.read_csv("indiv_mood_playlists/energy_mood_5_dataset.csv")

calm_songs_df= pd.read_csv("indiv_mood_playlists/calm_mood_dataset.csv")
calm_songs_df1= pd.read_csv("indiv_mood_playlists/calm_mood_1_dataset.csv")
calm_songs_df2= pd.read_csv("indiv_mood_playlists/calm_mood_2_dataset.csv")
calm_songs_df3= pd.read_csv("indiv_mood_playlists/calm_mood_3_dataset.csv")
calm_songs_df4= pd.read_csv("indiv_mood_playlists/calm_mood_4_dataset.csv")
calm_songs_df5= pd.read_csv("indiv_mood_playlists/calm_mood_5_dataset.csv")

angry_songs_df= pd.read_csv("indiv_mood_playlists/angry_mood_dataset.csv")
angry_songs_df1= pd.read_csv("indiv_mood_playlists/angry_mood_1_dataset.csv")
angry_songs_df2= pd.read_csv("indiv_mood_playlists/angry_mood_2_dataset.csv")
angry_songs_df3= pd.read_csv("indiv_mood_playlists/angry_mood_3_dataset.csv")
angry_songs_df4= pd.read_csv("indiv_mood_playlists/angry_mood_4_dataset.csv")
angry_songs_df5= pd.read_csv("indiv_mood_playlists/angry_mood_5_dataset.csv")


sad_df = pd.concat([sad_songs_df, sad_songs_df1, sad_songs_df2, sad_songs_df3, sad_songs_df4, sad_songs_df5])
happy_df = pd.concat([happy_songs_df, happy_songs_df1, happy_songs_df2, happy_songs_df3, happy_songs_df4, happy_songs_df5])
energy_df = pd.concat([energy_songs_df, energy_songs_df1, energy_songs_df2, energy_songs_df3, energy_songs_df4, energy_songs_df5])
calm_df = pd.concat([calm_songs_df, calm_songs_df1, calm_songs_df2, calm_songs_df3, calm_songs_df4, calm_songs_df5])
angry_df = pd.concat([angry_songs_df, angry_songs_df1, angry_songs_df2, angry_songs_df3, angry_songs_df4, angry_songs_df5])

def concatFrames(df1, df2, df3, df4, df5):
    df = pd.concat([df1,df2,df3,df4,df5], 
    ignore_index= True)
    return df

mood_data=concatFrames(sad_df, happy_df, energy_df, calm_df, angry_df)

mood_data_df = mood_data.sort_values(by = 'track')
mood_data_df = mood_data_df.reset_index(drop = True)

mood_data_df.to_csv(r".\spotify_mood_dataset.csv", index = False)
mood_data_df
