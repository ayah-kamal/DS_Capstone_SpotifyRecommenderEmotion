import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
from sklearn import preprocessing
import spacy

# Read csv of 50 most recently played songs of user
user_df = pd.read_csv('song_dataset.csv')
spotify_df = pd.read_csv('spotify_mood_dataset.csv')

# Remove songs that are added more than once in the same mood playlist
spotify_df = spotify_df.drop_duplicates(subset=['track', 'mood'], keep='first')

spotify_df.columns 
user_df.columns

print('Data type of each column of Dataframe :')
print(spotify_df.dtypes)
print(user_df.dtypes)

# change lyrics column type to string


# rename uri column on user_df and change format to match spotify_df
user_df.rename(columns={'uri': 'track_id'}, inplace= True)
user_df['track_id'] = user_df['track_id'].map(lambda x: x.lstrip('spotify:track:'))

mood_count_df = spotify_df.groupby('mood').nunique()
mood_count_df

# Cleaning the data (for lyrics NLP)
# remove all rows where lyrics are NaN
spotify_df.drop(spotify_df.index[spotify_df['lyrics'] == 'nan'], inplace=True)

# Text pre-processing
# Removing stop words (i.e: I, me, my, oh, yeah etc.)
# loading the english language small model of spacy
en = spacy.load('en_core_web_sm')
sw_spacy = list(en.Defaults.stop_words)
sw_spacy.extend(['oh', 'yeah', 'my', 'me',])
sw_spacy.extend(['[Intro]', '[Chorus]', 'my', 'me',])
print(sw_spacy)

# Methods to use:
## Topic Modeling
## bag-of-words model





# Normalising the Loudness
## All of the audio features are measured between 0 and 1
## Except Loudness which is measured between -60 and 0db
loudness = df[['loudness']].values
min_max_scaler = preprocessing.MinMaxScaler()
loudness_scaled = min_max_scaler.fit_transform(loudness)
df[['loudness']] = loudness_scaled

# Audio Feature Analysis
labels = list(df)[6:16]
features_df = df[['danceability',
 'energy',
 'key',
 'loudness',
 'speechiness',
 'acousticness',
 'instrumentalness',
 'liveness',
 'valence',
 'tempo']]

# Finding the correlation between all the audio features
scatter = sns.heatmap(features_df.corr(),  
annot=True,
linewidths=.5, cmap='RdPu')

# Find most recently listened to artist
