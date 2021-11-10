from lyrics_extractor import SongLyrics
import pandas as pd

spotify_df = pd.read_csv('indiv_mood_playlists/sad_mood_2_dataset.csv')

API_KEY = "AIzaSyC89x-y7FqEG4JcEWCU6OCG3IJaDk5yHC0"
GCS_ENGINE_ID = "d279e9fd8ba7ec0cb"

extract_lyrics = SongLyrics(API_KEY, GCS_ENGINE_ID)

extract_lyrics.get_lyrics(''+spotify_df['track'][4]+" "+spotify_df['artist'][4]+'')

lyrics = []

for i, x in enumerate(spotify_df['track']):
    try:
        print(spotify_df['track'][i], spotify_df['artist'][i])
        test = extract_lyrics.get_lyrics(''+spotify_df['track'][i]+" "+spotify_df['artist'][i]+'')
    except:
        test = 'NaN'
        pass
    lyrics.append(test)
    
spotify_df['lyrics'] = lyrics
spotify_df.to_csv(r"indiv_mood_playlists/sad_mood_2_dataset.csv", index = False)

spotify_df = pd.read_csv('indiv_mood_playlists/sad_mood_2_dataset.csv')
spotify_df



