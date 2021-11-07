import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
from sklearn import preprocessing

# Read csv of 50 most recently played songs of user
df = pd.read_csv('song_dataset.csv')

# Cleaning the data (for lyrics NLP)
# Removing stop words (i.e: I, me, my, oh, yeah etc.)
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
