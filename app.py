from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time, os
from secrets import *
from data_collection.dataCollection import *
from data_collection.lyricsScraping import *

TOKEN_INFO = "token_info"

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = "JsknfcsoO3495HNs"
app.config['SESSION_COOKIE_NAME'] = 'Ayah Cookie'

@app.route('/')
def login():
    if (os.path.exists('.cache')):
        os.remove('.cache')
    if (os.path.exists('song_dataset.csv')):
        os.remove('song_dataset.csv')
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external = True))

@app.route('/getUserTracks')
def getTracks():
    j_file = getJSONdata()
    # Create dataframe of track list with audio features
    # using dataCollection.py import
    df = get_album_tracks(j_file)
    df2_metadata = get_track_info(df)
    df1 = merge_frames(df, df2_metadata)
    song_df = lyrics_onto_frame(df1, df1['artist'])
    song_df.to_csv(r".\song_dataset.csv", index = False)
    return "Recently Played songs for user has been successfully exported to song_dataset.csv"

def getJSONdata():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external=False))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp.current_user_recently_played(limit=50)

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id= clientID,
        client_secret= clientSecret,
        redirect_uri= url_for('redirectPage', _external = True),
        scope = "user-read-recently-played ",
        show_dialog= True
    )



