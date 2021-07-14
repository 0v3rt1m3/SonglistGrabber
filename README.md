#Project is not maintained anymore. Web pages structure changes over time making it difficult to retrieve song lists anymore.

# SonglistGrabber
Grabs songs from site using XPATH for author and song name. Also has an added feature to get youtube links and download the videos of the song. It includes the feature to convert the videos downloaded to mp3.

# Requirements
Install python 3 <a href='https://www.python.org/downloads/'> here</a><br>
*Make sure to have pip when installing python<br>
Install ffmpeg get it <a href='https://ffmpeg.zeranoe.com/builds/'>here</a>
### How to check if installed properly
![Check Installation](https://github.com/0v3rt1m3/SonglistGrabber/blob/master/sample_runs/to_check_requirements.gif "Check Installation")
# Installation
1. Download or clone the repo.
2. Extract zip and go to root folder.
3. Run Command Prompt or Command Line and go to the current directory of the extracted folder.
4. Run `pip install -r requirements.txt`
5. Downloaded files goes to path /mp4 for mp4 files that are audio only and path /mp3 for mp3 files.

### Sample Installation and Run
![Sample Installation](https://github.com/0v3rt1m3/SonglistGrabber/blob/master/sample_runs/sample_install_and_run.gif "Sample Installation")
# Add your own sites
 1. open siteinfo.py using your text editor.
 2. edit this line {'url': 'insertYourURLhere', 'XPATHsong': 'insertXpathSongTitle','XPATHauthor':'insertXpathAuthor'}
 3. Make sure that your xpath to song title and author/singer is correct.
 
 
