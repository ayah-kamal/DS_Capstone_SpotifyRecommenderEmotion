from bs4 import BeautifulSoup
import requests
import concurrent.futures

uri = "http://localhost:5000/"
genius_key = "rCoFyb4ZLVz_BuuD1tIZLp9Io0FQ33-txnvo25KlDZHon9GmEEeNXl4-MVxREhkd"

#function to scrape lyrics from genius
def scrape_lyrics(artistname, songname):
    artistname2 = str(artistname.replace(' ','-')) if ' ' in artistname else str(artistname)
    songname2 = str(songname.replace(' ','-')) if ' ' in songname else str(songname)
    page = requests.get('https://genius.com/'+ artistname2 + '-' + songname2 + '-' + 'lyrics')
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics1 = html.find("div", class_="lyrics")
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")

    if lyrics1:
        lyrics = lyrics1.get_text()
    elif lyrics2:
        lyrics = lyrics2.get_text()
    elif lyrics1 == lyrics2 == None:
        lyrics = None
    return lyrics

#function to attach lyrics onto data frame
#artist_name should be inserted as a string
def lyrics_onto_frame(df1, artist_name):
   # with concurrent.futures.ThreadPoolExecutor(max_workers=len(df1['track'])) as executor:
        for i,x in enumerate(df1['track']):
            test = scrape_lyrics(artist_name[i], x)
            df1.loc[i, 'lyrics'] = test
        return df1

# # blonde_df1_tracks = get_album_tracks('spotify:album:3mH6qwIy9crq0I9YQbOuDf')
# # blonde_df2_metadata = get_track_info(blonde_df1_tracks)
# # df1 = merge_frames(blonde_df1_tracks, blonde_df2_metadata)
# # lyrics_onto_frame(df1, 'frank ocean')

