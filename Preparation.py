import pandas as pd
import numpy as np
from sklearn import preprocessing
from collections import Counter
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string

# Read csv of 50 most recently played songs of user
user_df = pd.read_csv('pre-processed dataset\song_dataset.csv')
spotify_df = pd.read_csv('pre-processed dataset\spotify_mood_dataset.csv')

# Remove songs that are added more than once in the same mood playlist
spotify_df = spotify_df.drop_duplicates(subset=['track','artist','mood'], keep='first').reset_index(drop= True)

"""spotify_df.columns 
user_df.columns"""

# rename uri column on user_df and change format to match spotify_df
user_df.rename(columns={'uri': 'track_id'}, inplace= True)
user_df['track_id'] = user_df['track_id'].map(lambda x: x.lstrip('spotify:track:'))

# Cleaning the data (for lyrics NLP)
# remove all rows where lyrics are NaN
spotify_df = spotify_df[spotify_df["lyrics"].notna()]

mood_count_df = spotify_df.groupby('mood').nunique()
mood_count_df

# Text pre-processing
# extracting lyrics without headers ([Intro], [Chorus] etc.)
translator = str.maketrans('', '', string.punctuation)
def split_text(x):
   text = x['lyrics']
   sections = text.split('\\n\\n')
   keys = {'Intro':np.nan, 'Verse 1': np.nan,'Verse 2':np.nan,'Verse 3':np.nan,'Verse 4':np.nan, 'Chorus':np.nan, 'Outro': np.nan,
   'Bridge':np.nan, 'Refrain':np.nan, 'Chorus 1': np.nan, 'Chorus 2': np.nan, 'Pre-Chorus': np.nan, 'Part 1': np.nan, 'Part 2': np.nan,
   'Post-Chorus': np.nan, 'Chorus with Refrain repeating': np.nan, 'Pre-Chorus 1': np.nan, 'Pre-Chorus 1': np.nan}
   lyrics = str()
   single_text = []
   res = {}
   for s in sections:
       key = s[s.find('[') + 1:s.find(']')].strip()
       if ':' in key:
           key = key[:key.find(':')]
       if key in keys:
           single_text += [x.lower().replace('(','').replace(')','').translate(translator) for x in s[s.find(']')+1:].split('\\n') if len(x) > 1]
       res['single_text'] =  ' \n '.join(single_text)
       if key not in keys:
           single_text += [x.lower().replace('(','').replace(')','').translate(translator) for x in s[s.find(']')+1:].split('\\n') if len(x) > 1]
       res['single_text'] =  ' \n '.join(single_text)
   return pd.Series(res)

spotify_df = spotify_df.join( spotify_df.apply(split_text, axis=1))
spotify_df['single_text'].replace('', np.nan, inplace=True)

# Remove rows that where lyrics weren't extracted
spotify_df = spotify_df[spotify_df["single_text"].notna()].reset_index(drop= True)

# Tokenization 
spotify_df["single_text"].apply(word_tokenize)

# Removing stop words (i.e: oh, yeah, got etc.)
en_stopwords = stopwords.words('english')
en_stopwords.extend(['im', 'got',  'oh', 'yeah', 'ooh',
"youre", "youve", "youll", "youd", "shes", "thatll", "dont", "shouldve","arent",  "couldnt",  "didnt",  "doesnt",  "hadnt", "hasnt",  "havent", "isnt", "mightnt",  "mustnt", "neednt",  "shant", "shouldnt",  "wasnt",  "werent",  "wont",  "wouldnt"])
spotify_df["single_text"] = spotify_df["single_text"].apply(lambda x: ' '.join([word for word in x.split() if word not in (en_stopwords)]))

Counter(" ".join(spotify_df["single_text"]).split()).most_common(10)

# Normalising the Loudness
## All of the audio features are measured between 0 and 1
## Except Loudness which is measured between -60 and 0db
def scale_loudness(df):
    loudness = df[['loudness']].values
    min_max_scaler = preprocessing.MinMaxScaler()
    loudness_scaled = min_max_scaler.fit_transform(loudness)
    df[['loudness']] = loudness_scaled

scale_loudness(spotify_df)

spotify_df.head()
spotify_df.to_csv(r"./processed_spotify_dataset.csv", index = False)

# Repeat steps for user dataset
user_df = user_df.join(user_df.apply(split_text, axis=1))
user_df['single_text'].replace('', np.nan, inplace=True)

# Remove rows that where lyrics weren't extracted
user_df = user_df[user_df["single_text"].notna()].reset_index(drop= True)

# Tokenization 
tokenizer = RegexpTokenizer(r'\w+')
user_df["single_text"].apply(tokenizer.tokenize)

# Removing stop words (i.e: oh, yeah, got etc.)
en_stopwords.extend(['intro', 'verse', 'chorus', 'outro'])
user_df["single_text"] = user_df["single_text"].apply(lambda x: ' '.join([word for word in x.split() if word not in (en_stopwords)]))

Counter(" ".join(user_df["single_text"]).split()).most_common(10)

# Normalising the Loudness
scale_loudness(user_df)

user_df.head()
spotify_df.to_csv(r"./processed_user_dataset.csv", index = False)
