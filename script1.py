
import requests
from bs4 import BeautifulSoup
import csv
from requests_html import HTMLSession
import youtube_dl

url = []
# single song
url.append("https://open.spotify.com/playlist/5E3NXMAqqEPdYw3gAx1fhf?si=0414dcb8fa334a7c")
# post malone playlist
url.append("https://open.spotify.com/playlist/1OdPh4SDEGM1xM0lCcqObn?si=be9593494fa54d8d")
# jack harlow playlist
url.append("https://open.spotify.com/playlist/1Cx4SxOKDwqGw5oo1tF3Ii?si=e491b210c41a48ae")
# russ playlist
url.append("https://open.spotify.com/playlist/6CjlyN0rMq80w1JdUcIW6p?si=abd86563b6a0440e")
# owlrana
url.append("https://open.spotify.com/playlist/0pP5Ynm92wQsINABrCjIAp?si=c3dc0efb077c44c1")

# Set which URL you want to parse from list
r = requests.get(url[0])
soup = BeautifulSoup(r.content, 'html5lib')

# get title of all songs
def getSongs():
    songs = []
    songsTags = soup.findAll('div', attrs = {'class':'tracklist-col name'})
    
    for song_tag in songsTags:
        title = (song_tag.find('span', attrs = {'class':'track-name'}).text)
        artist = (song_tag.find('span', attrs = {'class':'artists-albums'}).find('span', attrs = {'dir':'auto'}).text)
        songs.append((title, artist))
                
    return songs

songs = getSongs()

# generate name of query for YouTube
def ytQueryUrls():
    # store all links
    links = []
    
    for song in songs:
        title = song[0].replace(' ', '+').replace('\'', '%27')
        artist = song[1].replace(' ', '+').replace('\'', '%27')
        YTQR = title + "+" + artist + "+" + "lyrics"
        YTQR = "https://www.youtube.com/results?search_query=" + YTQR
        links.append(YTQR)

    return links

ytLinks = ytQueryUrls()

# Function that can download YouTube Videos
def download(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    

#Extract the URL of first youtube element and create y2mate url
def mp3Pages():
    mp3Pages = []
    session = HTMLSession()

    for ytLink in ytLinks:
        url = ytLink
        response = session.get(url)
        response.html.render()

        for links in response.html.find('a#video-title'):
            link = next(iter(links.absolute_links))
            break

        if link not in mp3Pages:
            mp3Pages.append(link)
            
        print(link)
    
    mp3Pages = list(set(mp3Pages))
    return mp3Pages


mp3Pages = mp3Pages()
#print(mp3Pages)

print("Number of songs: ", len(songs))
print("Number of YouTube links: ", len(ytLinks))
print("Number of mp3 Pages: ", len(mp3Pages))

for song in mp3Pages:
    download(song)