from bs4 import BeautifulSoup
import requests
from lyricsgenius import Genius

uri = "http://localhost:5000/"
genius_key = "9rXoiyhZUYHiTC_-KU7_gTP5nb8okqTxL-O2g0HhFBjMS_8sAUkqR1vHexTO8LVe"

#function to scrape lyrics from genius
def scrape_lyrics(artistname, songname):
    genius = Genius(genius_key)
    #genius.verbose = False
    genius.remove_section_headers = True    
   
    artistname2 = str(artistname.replace(' ','-')) if ' ' in artistname else str(artistname)
    artistname2 = str(artistname2.replace("'",''))
    artistname2 = str(artistname2.replace(".",''))
    print(artistname2)
    songname2 = str(songname.replace(' ','-')) if ' ' in songname else str(songname)
    songname2 = str(songname2.replace("'",'')) 
    print(songname2)
    page = requests.get('https://genius.com/'+ artistname2 + '-' + songname2 + '-' + 'lyrics')
    html = BeautifulSoup(page.text, 'html.parser')

    lyrics1 = html.find("div", class_="lyrics")
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")

    if lyrics1:
        lyrics = lyrics1.get_text()
       # lyrics = re.sub('[Verse]','',lyrics) # Remove [Verse] and [Bridge] stuff 
    elif lyrics2:
        lyrics = lyrics2.get_text()
      #  lyrics = re.sub('[Verse]','',lyrics) # Remove [Verse] and [Bridge] stuff 
    elif lyrics1 == lyrics2 == None:
        artist = genius.search_artist(artistname,max_songs=1)
        song = artist.song(songname)
        if song == None:
            return None
        else:
            return song.lyrics
    return lyrics


#function to attach lyrics onto data frame
#artist_name should be inserted as a string
def lyrics_onto_frame(df1, artist_name):
   # with concurrent.futures.ThreadPoolExecutor(max_workers=len(df1['track'])) as executor:
        for i,x in enumerate(df1['track']):
            test = scrape_lyrics(artist_name[i], x)
            df1.loc[i, 'lyrics'] = test
        return df1


    





