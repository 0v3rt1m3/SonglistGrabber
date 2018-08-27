from urllib.request import urlopen
import urllib.request
import glob, os
from pytube import YouTube
from lxml import etree
import json
import subprocess
from bs4 import BeautifulSoup
from siteinfo import SITE_LIST

class Song:

    def __init__(self, songTitle="", singer="", queryString="", links=[], unsuccessfulLinks=[]):
        self.songTitle = songTitle
        self.singer = singer
        self.queryString = queryString
        self.links = links
        self.unsuccessfulLinks = unsuccessfulLinks

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.queryString == other.queryString

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    def getLinks(self):

        print(self.queryString.encode("ascii", errors="ignore").decode())
        page = urlopen(self.queryString.encode("ascii", errors="ignore").decode())
        soup = BeautifulSoup(page, 'html.parser')
        divs = soup.find_all("div", {"class": "yt-lockup-content"})
        link = []
        for i in divs:
            href = i.find('a', href=True)
            if self.songTitle.lower() in href.text.lower():
                link.append("https://www.youtube.com" + href['href'])
        return link

    def downloadSongs(self):
        for link in self.links:
            try:

                cwd = os.getcwd()
                yt = YouTube(link)
                title = yt.title
                print("Starting to download " + title)
                stream = yt.streams.filter(only_audio=True, file_extension = "mp4")
                stream.last().download(cwd.replace("\\", "/"))
                print("Finished downloading " + title)

            except:
                print("Next Link")
                pass
            else:
                print("Success")
                return True

        return False

    def convertToMP3(self):
        for title in glob.glob("*.mp4"):
            try:
                title = title.replace(".mp4","")
                cwd = os.getcwd()
                titleConvMP4 = '"' + title + '.mp4"'
                titleConvMP3 = '"' + title + '.mp3"'
                srcMP4 = cwd + "\\" + title + ".mp4"
                destMP4 = cwd + "\\" + "mp4" + "\\" + title + ".mp4"
                srcMP3 = cwd + "\\" + title + ".mp3"
                destMP3 = cwd + "\\" + "mp3" + "\\" + title + ".mp3"
                command = "ffmpeg -i " + titleConvMP4 + " -vn -b:a 128k -c:a libmp3lame " + titleConvMP3

                print("Start converting to mp3: " + title)
                subprocess.call(command, shell=True)
                os.rename(srcMP4, destMP4)
                os.rename(srcMP3, destMP3)
                print("Converted Successfully")
            except:
                print("Existing delete")
                pass

class MusicSite():
    songlist = []

    def __init__(self, url, XPATHsong, XPATHauthor):
        self.url = url
        self.XPATHsong = XPATHsong
        self.XPATHauthor = XPATHauthor
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        self.response = urlopen(req)
        self.htmlparser = etree.HTMLParser()
        self.tree = etree.parse(self.response, self.htmlparser)

        with open('data.json') as f:
            songlists = json.load(f)
            for song in songlists:
                if 'links' in song:
                    # def __init__(self, songTitle, singer, queryString, links=[], unsuccessfulLinks=[]):
                    self.songlist.append(Song(song['songTitle'],song['singer'],song['queryString'],song['links']))
                elif 'links' in song and 'unsuccessfulLinks' in song:
                    self.songlist.append(Song(song['songTitle'], song['singer'], song['queryString'], song['links'],song['unsuccessfulLinks'] ))
                else:
                    self.songlist.append(Song(song['songTitle'], song['singer'], song['queryString']))

    def getSongsAuthor(self):
        results = self.tree.xpath(self.XPATHsong)
        songs = []
        listOfSongs = []
        for result in results:
            if result.text is not None:
                songs.append(result.text.replace("\n",""))
                song = Song()
                song.songTitle = result.text.replace("\n","")
                listOfSongs.append(song)

        results = self.tree.xpath(self.XPATHauthor)
        i = 0
        j = 0
        for result in results:
            if result.text is not None:
                query = "https://www.youtube.com/results?search_query=" + songs[j] + " " + result.text.replace("\n","") + " lyrics"
                query = query.replace(" ", "+").replace("\n","")
                listOfSongs[i].singer = result.text.replace("\n","")
                listOfSongs[i].queryString= query
            else:
                listOfSongs.pop(i)
                i= i-1
            j= j + 1
            i = i + 1

        #
        for song in listOfSongs:
            if song not in self.songlist:
                song.links = song.getLinks()
                self.songlist.append(song)
                if song.downloadSongs():
                    song.convertToMP3()
                    self.songlist.append(song)
                    print("new Song added: " + song.songTitle)
                    with open('data.json', 'w') as outfile:
                        json.dump([ob.__dict__ for ob in self.songlist], outfile)


    def getSearchQueries(self):
        for song in self.songlist:
            print(song.songTitle)



def main():

    # print(cwd)
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # print(dir_path)
    print("start")
    for site in SITE_LIST:
        musicsite = MusicSite(site['url'],site['XPATHsong'],site['XPATHauthor'])
        musicsite.getSongsAuthor()
        musicsite.getSearchQueries()


    # musicsite = MusicSite("https://www.ranker.com/list/best-indie-songs-2018/ranker-music",
    #                       "//*[contains(@class, 'listItem__title')]",
    #                       "//*[contains(@class, 'listItem__properties black default')]")



    # musicsite = MusicSite("https://www.billboard.com/charts/pop-songs",
    #                       "//*[contains(@class, 'chart-list-item__title-text')]",
    #                       "//*[contains(@class, 'chart-list-item__artist')]")

    print("end")
    # response = urlopen("https://www.billboard.com/charts/hot-100")

    # url = "https://www.ranker.com/list/best-indie-songs-2018/ranker-music"
    # response = urlopen(url)
    # htmlparser = etree.HTMLParser()
    # tree = etree.parse(response, htmlparser)
    #
    # results = tree.xpath("//*[contains(@class, 'listItem__title')]")
    # for result in results:
    #     print(result.text)


if __name__ == "__main__":
    main()
