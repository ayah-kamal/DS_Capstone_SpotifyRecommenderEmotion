from bs4 import BeautifulSoup
import requests, random, time
from random import randrange
from lyricsgenius import Genius
from secrets import *

uri = "http://localhost:5000/"

USER_AGENT_SCRAPER_BASE_URL = 'http://www.useragentstring.com/pages/useragentstring.php?name='

POPULAR_BROWSERS = ['Chrome', 'Firefox', 'Mozilla', 'Safari', 'Opera', 'Opera Mini', 'Edge', 'Internet Explorer']

def get_user_agent_strings_for_this_browser(browser):
    """
    Get the latest User-Agent strings of the given Browser
    :param browser: string of given Browser
    :return: list of User agents of the given Browser
    """

    url = USER_AGENT_SCRAPER_BASE_URL + browser
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    user_agent_links = soup.find('div', {'id': 'liste'}).findAll('a')[:20]

    return [str(user_agent.text) for user_agent in user_agent_links]


def get_user_agents():
    """
    Gather a list of some active User-Agent strings from
    http://www.useragentstring.com of some of the Popular Browsers
    :return: list of User-Agent strings
    """

    user_agents = []
    for browser in POPULAR_BROWSERS:
        user_agents.extend(get_user_agent_strings_for_this_browser(browser))
    return user_agents[3:] # Remove the first 3 Google Header texts from Chrome's user agents

proxy_user_agents = get_user_agents()

#function to scrape lyrics from genius
def scrape_lyrics(artistname, songname):
    genius = Genius(genius_key)
    #genius.verbose = False
    genius.remove_section_headers = True    

    # To randomly select an User-Agent from the collected user-agent strings
    random_user_agent = random.choice(proxy_user_agents)
    headers = {"User-Agent": random_user_agent}
  
    #Make the request
    artistname2 = str(artistname.replace(' ','-')) if ' ' in artistname else str(artistname)
    artistname2 = str(artistname2.replace("'",''))
    artistname2 = str(artistname2.replace(".",''))
    #print(artistname2)
    songname2 = str(songname.replace(' ','-')) if ' ' in songname else str(songname)
    songname2 = str(songname2.replace("'",'')) 
    songname2 = str(songname2.replace("(",'')) 
    songname2 = str(songname2.replace(")",'')) 
    songname2 = str(songname2.replace("!",'')) 
    #print(songname2)
    page = requests.get('https://genius.com/'+ artistname2 + '-' + songname2 + '-' + 'lyrics', headers)
    html = BeautifulSoup(page.text, 'html.parser')

    lyrics1 = html.find("div", class_="lyrics")
    time.sleep(randrange(5,15))
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
    time.sleep(randrange(5,15))

    if lyrics1:
        lyrics = lyrics1.get_text()
       # lyrics = re.sub('[Verse]','',lyrics) # Remove [Verse] and [Bridge] stuff 
    elif lyrics2:
        lyrics = lyrics2.get_text()
      #  lyrics = re.sub('[Verse]','',lyrics) # Remove [Verse] and [Bridge] stuff 
    elif lyrics1 == lyrics2 == None:
        artist = genius.search_artist(artistname,max_songs=1)
        time.sleep(randrange(5,20))
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



    





