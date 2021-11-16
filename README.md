![alt text](https://djmag.com/sites/default/files/article/image/Header-1280x489%20%281%29_0.png)
# :notes: Spotify Recommendation Playlist Based on the Emotion of Users Most Recently Played Songs - (DSI Capstone Project)
This project serves as the final capstone project for the MiSK Data Science immersive program. The final HTML website of the project can be viewed [here](https://ayah-kamal.github.io/DS_Capstone_SpotifyRecommenderEmotion/spotifyRecommend.html).

<!--ts-->
Table of contents
=================
- [Background](#background)
  - [Spotify Audio Features](#spotify-audio-features)
  - [Lyrics](#lyrics)
- [Usage](#usage)
 <!--te-->

## Background
This project aims to recommend songs to a user based on the mood of their most recently played songs on Spotify. There are two datasets that are obtained:
- **Spotify Mood Dataset**: contains around 2600 songs from 13 playlists from Spotify that are created by Spotify or other Spotify users. These playlists are created by mood. The moods that were obtained and will be observed are: Happy, Sad, Angry, Calm, and Energy. 
- **User Recently Played Dataset**: this dataset is obtained from the user and contains the 50 most recently played songs. To obtain this dataset, the user must give our app authorization. The installation and setting up of this is discussed [here](#usage).

To determine the mood of the song two variables for each track will be observed. The first is the valence of the track from the Spotify API audio features, the other is the lyrics of the track. These two variables are chosen specifically because choosing one or the other is usually not enough to determine the mood of the song, which can be considered specific to the user. Especially in cases where the lyrics of the song do not match the audio mood (valence) of the track. A popular example of a song like this is [Take a Walk by Passion Pit](https://www.youtube.com/watch?v=dZX6Q-Bj_xg), which is an upbeat happy sounding song with sad lyrics. On the flip side, a popular sad/mellow song that has hopeful/happy lyrics is [Don't Panic by Coldplay](https://www.youtube.com/watch?v=yWeuUwpEQfs).

### Spotify Audio Features:
Spotify uses a series of different features to classify tracks.
- **Acousticness:** A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
- **Danceability:** Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
- **Energy:** Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
- **Instrumentalness:** Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
- **Liveness:** Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides a strong likelihood that the track is live.
- **Loudness:** the overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing the relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.
- **Speechiness:** Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audiobook, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
- **Valence:** A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
- **Tempo:** The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, the tempo is the speed or pace of a given piece and derives directly from the average beat duration. [[1]](https://developer.spotify.com/discover/)[[2]](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)

### Lyrics:
Lyrics are not available on Spotify, so to obtain the lyrics of the tracks mutliple methods were used. 
- **Genius API**: Genius.com is one of the most popular and biggest collection of song lyrics and musical knowledge. They provide a [Genius API](https://docs.genius.com/) that makes utilizing their website much easier for developer. Additionally, using the [genius package](https://pypi.org/project/lyricsgenius/) (`lyricsgenius`) created for Python simplifies the process further by providing Python methods for the Genius API.
- **Web-scraping from Genius**: Similiary, Genius.com is web-scraped using the Python package [BeatifulSoup4](https://pypi.org/project/beautifulsoup4/). Web scraping is used first and if it's unsuccessful we resort to using the genius package, this is because the genius package runs very slowly. 
- **lyrics-extractor library**: For the Spotify mood playlist dataset, the [lyrics-extractor](https://pypi.org/project/lyrics-extractor/) library for Python is used, as it scrapes from AZLyrics, which is more lenient when it comes to being blocked while scraping. 

## Usage
### Spotify API:
To be able to use the Spotify API and access a users information, you will need to register an app and get your own credentials from the Spotify for Developers Dashboard. To do so, go to  [your Spotify for Developers Dashboard](https://beta.developer.spotify.com/dashboard) and create your application. For the examples, we registered these Redirect URIs: http://localhost:5000 

Once you have created your app, replace the `clientID`, `redirect_uri` and `clientSecret` in the secrets.py with the ones you get from My Applications.

### Genius API:
Similiar to the Spotify API, the Genius API requires you generate your own special key (Client Access Token) to gain access to the API, which we use in the genius package. To get your necessary Genius API keys, you need to navigate to the [Genius API Developers page](https://genius.com/api-clients). The following URL goes into step-by-step detail into how to get your personal API key: https://melaniewalsh.github.io/Intro-Cultural-Analytics/04-Data-Collection/07-Genius-API.html.

Once you've obtained the key, replace it into `genius_key` in the secrets.py file.

### Getting your 50 most recently played songs:
Now that you have all the necessary credentials, you can obtain your 50 most recently played songs or even any other users 50 most recently played songs (as long as they give you the authorization). Which leads us to the next step, to get authorization from a user a Flask app was created that opens on a local host and asks you to allow authorization as shown below:

![Screenshot (4)](https://user-images.githubusercontent.com/68741119/141888632-b122b253-c799-4d13-9d1f-1a8b96ce728c.png)

It takes a while for the app to run as it is also scraping the lyrics for the songs but after it successfully runs it will display a blank page with a message saying:
> Recently Played songs for user has been successfully exported to song_dataset.csv

To run the flask app, make sure you are in the same directory as your project folder. Then, from the terminal run the command:

`flask run`

If successfully run, it should give you a link to the local host URL.
