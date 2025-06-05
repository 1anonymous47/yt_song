# import urllib.request as res
# import re
# from collections import OrderedDict

# data = res.urlopen("https://www.youtube.com/results?search_query=tbi+nr")

# data = data.read().decode()


# videoid = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', data)  # Added _ and - just in case



# videoid = list(OrderedDict.fromkeys(videoid))
# print(videoid)
import yt_dlp

ytlopts={
    'format':'bestaudio/best',
    'outtmpl':'src\\static\\audios\\%(id)s.%(ext)s',
}

url = "https://www.youtube.com/watch?v=6RMTt-LakoI"
with yt_dlp.YoutubeDL(ytlopts) as ydl:
    info = ydl.extract_info(url,download=False)
    tittle = info["title"]
    thumbnail = info["thumbnail"]
    temp = info['formats']
    audiosrc = ""
    for i in range(len(temp)):
        if(temp[i]['audio_ext']!="none" and temp[i]['audio_ext']=="webm"):
            audiosrc=temp[i]['url']
    print(tittle,thumbnail,audiosrc)