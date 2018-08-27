# url = website url that contains list of songs
# XPATHsong = xpath that contains the song
# XPATHauthor = xpath that contains the author

SITE_LIST = [
    {'url': 'https://www.ranker.com/list/best-indie-songs-2018/ranker-music',
     'XPATHsong': "//*[contains(@class, 'listItem__title')]",
     'XPATHauthor': "//*[contains(@class, 'listItem__properties black default')]"},

    # Supports multiple list of songs
    # {'url': 'http://www.popvortex.com/music/charts/top-indie-songs.php',
    #  'XPATHsong': '//div/p/cite/a',
    #  'XPATHauthor':'//div/p/em'},
    #


    # Uncomment next line and add more dictionaries if you want to download many.
    #{'url': 'addUrl', 'XPATHsong': 'insertXpathSong','XPATHauthor':'insertXpathAuthor'},
]