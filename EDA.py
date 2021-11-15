import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
from sklearn.preprocessing import LabelEncoder
from wordcloud import WordCloud
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Preparing Data
# Read csv of 50 most recently played songs of user
user_df = pd.read_csv('.\processed dataset\processed_user_dataset.csv')
# Read csv of spotify mood playlist dataset
spotify_df = pd.read_csv('.\processed dataset\processed_spotify_dataset.csv')

frames = [user_df,spotify_df]
# first 50 rows are the users recently played
df = pd.concat(frames)

df.shape
'''
The dataset contains 12 columns that we can use for exploratory analysis. Since we have already cleaned the dataset,
there is not alot of observed NaN values. Howeverm we will check to see:
'''

msno.matrix(df)
plt.show()
'''
We can see that there are only two columns with missing values (noting that the first 50 rows are the users recently listened)
played_at is null for the spotify dataset as it does not exist so we will keep the NaN values. On the other hand, the mood is
null for the users songs, as this is information we currently don't have and will be predicting.
'''

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

# showing distribution of each audio feature across all the observations
features_df.hist(figsize = (15,15))
plt.show()

# Finding the correlation between all the audio features
scatter = sns.heatmap(features_df.corr(),  
annot=True,
linewidths=.5, cmap='RdPu')
'''
We can see that there is the highest correlation between energy-loudness and valence-energy.
While, we see there is an anti-correlation between acousticness-energy and acousticness-loudness.
Both of these results are logical
'''

artists = df.artist.value_counts()
pd.DataFrame(pd.DataFrame(df.groupby(df['artist']).
filter(lambda x: len(x)>10)).groupby("artist").energy.mean()).sort_values(by='energy',ascending=False)[:20]
df.loc[df['artist'] == 'City Morgue', 'track']
'''
If we disclude various artists, $uicideboy$ is the most occuring artist in our dataset,
however, City Morgue has the most energetic songs and appears 26 times in our dataset
'''

pd.DataFrame(pd.DataFrame(df.groupby(df['artist']).
filter(lambda x: len(x)>10)).groupby("artist").loudness.mean()).sort_values(by='loudness',ascending=False)[:20]
df.loc[df['artist'] == 'Little Mix', 'track']
'''
Even though we have a high correlation between loudness and energy, we can see that the artist with
the loudest songs is Little Mix who appear in the dataset 17 times.
'''

# 2-D scatter plot to visualize tendencies using some audio features, 
# specifically the "energy" and "danceability" features
# The red cross represents the "average popular song"'s audio features
average_noise = user_df['energy'].mean()
average_danceability = user_df['danceability'].mean()
plt.scatter(spotify_df['danceability'],spotify_df['energy'],alpha=0.75)
plt.axhline(y=average_noise, color='r')
plt.axvline(x=average_danceability, color='r')
plt.title("Energy as a function of Danceability - from my music library")
plt.xlabel("Danceability")
plt.ylabel("Energy")
plt.show()
'''
Here we're comparing the users tendency to listen to songs that have energy and tendency compared to the
Spotify dataset. We can see that the songs in the Spotify dataset generally have high energy and danceability.
While the user (red cross) listens to songs that are higher in energy than danceability
'''

# Finding the correlation between all the audio features(continuous) and the mood(categorical)
enc = LabelEncoder()
spotify_df['mood_enc'] = enc.fit_transform(spotify_df['mood'])

corr = spotify_df.iloc[:, :-1].corr()
sns.heatmap(corr,
            xticklabels=corr.columns,
            yticklabels=corr.columns,
            annot=True,
            linewidths=.2,)
plt.show()
'''
0 - Angry
1 - Calm
2 - Energy
3 - Happy
4 - Sad
'''

# NLP on Lyrics
# Word cloud of user dataset lyrics vs. spotify dataset lyrics
wordcloud_spotify = WordCloud().generate(' '.join(spotify_df['single_text']))
plt.imshow(wordcloud_spotify)
plt.axis("off")
plt.show()

wordcloud_spotify = WordCloud().generate(' '.join(user_df['single_text']))
plt.imshow(wordcloud_spotify)
plt.axis("off")
plt.show()
'''
It's hard to conclude the sentiment of the lyrics overall by looking at their 
wordclouds. We will assign a sentiment to each song ranging from negative to neutral to positive.
To do this we will perform sentiment analysis using textblob.

These sentiments will help us identify the mood better:
Positive: Energy and Happy (0.3 - 1.0)
Neutral: Calm (-0.35 - 0.3)
Negative: Sad and Angry (-1.0 - -0.35)
'''
filter_values = [-1, -0.35, 0.3, 1]   

def sentiment_func(lyrics):
    try:
        return TextBlob(lyrics).sentiment
    except:
        return None

df['sentiment'] = df['single_text'].apply(sentiment_func)
df['sentiment'][0][0]
df['polarity'] = df['sentiment'].apply(lambda x: x[0])

df = df.drop(columns= 'sentiment')
df['sentiment'] = pd.cut(df['polarity'], bins=filter_values, 
                                     labels=['negative', 'neutral', 'positive'])
'''
We won't be looking at subjectivity.
Polarity is a float that lies between [-1,1], 
-1 indicates negative sentiment and +1 indicates positive sentiments. 
However, by observing the results TextBlob does not always provide the expected results.
So, we'll use VaderSentiment which gives a more detailed breakdown and compare the two.
''' 
analyzer = SentimentIntensityAnalyzer()
df['v_sentiment'] = df['single_text'].apply(analyzer.polarity_scores)
df = pd.concat([df.drop(['v_sentiment'], axis=1), df['v_sentiment'].apply(pd.Series)], axis=1)


df['v_sentiment'] = pd.cut(df['compound'], bins=filter_values, 
                                     labels=['negative', 'neutral', 'positive'])

'''
Vader performs much better at predicting negative sentiment, however it also over exaggerates the 
neutrals and sometimes negatives to positive sentiments. After observing and comparing, we see that Vader
is better at predicting Energy songs as positive and Angry songs as negatives, which are our extremes 
at both ends, but TextBlob is better at prediciting Calm songs as neutral. Both perform around the same
for Happy and Sad Songs. However, if we take into consideration that the mood does not always match the
sentiment of lyrics, we can conclude that that it can sometimes make sense for the mood not to match
the sentiment. 

For example, Taylor Swifts 'Bad Blood' has a mood of Energy but the lyrics have a negative sentiment for 
both Vader and TextBlob and this can be because the lyrics contain lyrics such as 'bad', 'sad', 'mad'
etc. which are recognized as negative words.
'''
# by observing and comparing the two lexicons, we cna conclude that Vader performs better than TextBlob except in
# Calm songs, but thats because TextBlob tends to classify most of the songs as calm
df.groupby(["mood", "sentiment", "v_sentiment"]).size().reset_index(name="count")

# we will drop TextBlob and use Vader
df = df.drop(columns= ['sentiment','neg','pos','neu', 'polarity'])
df.rename(columns={'v_sentiment': 'sentiment', 'compound': 'polarity'}, inplace= True)

'''
So we will be looking at both the valence of the song as well as its sentiment to recommend the songs to the user.
Noting that valence is defined by spotify as Valence: A measure from 0.0 to 1.0 describing the musical positiveness 
conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), 
while tracks with low valence sound more negative (e.g. sad, depressed, angry).

So, by looking at both the audio feature and sentiment we can better determine the mood of the user's most recently
listened to songs.
'''

