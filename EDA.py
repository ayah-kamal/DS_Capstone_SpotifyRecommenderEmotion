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

# Visualizing which artists appear most in the dataset for the user


# Finding the correlation between all the audio features
scatter = sns.heatmap(features_df.corr(),  
annot=True,
linewidths=.5, cmap='RdPu')

# Find most recently listened to artist