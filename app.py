import yt_dlp
from flask import Flask,render_template,request,jsonify,redirect, url_for,make_response
import urllib.request
import re

from collections import OrderedDict
from flask_cors import CORS 
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager,set_access_cookies



app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_SECURE'] = False  # Set to True only with HTTPS
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disable CSRF just for testing


jwt = JWTManager(app)

database = ['user1','user2']

songdetails = {}
playlist = {}



# songdetails = {}
# playlist = {
# }

CORS(app)
            

ytlopts={
    'format':'bestaudio/best',
    'outtmpl':'static\\audios\\%(id)s.%(ext)s',
}

@app.route('/writer')
def writer():
    f = open("songdetails.txt",'w')
    f.write(str(songdetails))
    f = open("playlist.txt",'w')
    f.write(str(playlist))
    f = open("database.txt",'w')
    f.write(str(database))
    print(songdetails)
    print()
    print(playlist)
    print()
    print(database)
    return "Writed"

@app.route('/reader')
def reader():
    f = open("songdetails.txt",'r')
    songdetails = f.read
    print(songdetails)
    f = open("playlist.txt",'r')
    playlist = f.read()
    f = open("database.txt",'r')
    database = f.read()
    print(songdetails)
    print()
    print(playlist)
    print()
    print(database)
    return "Readed"
@app.route('/')
def printer():
    return jsonify({"Users":database,"Songdetails":songdetails,"Playlists":playlist})

#WEBPAAGES
@app.route('/downloaderpage')
def downloaderpage():
    return render_template('downloader.html')

@app.route('/playlisterpage')
def playlisterpage():
    return render_template('playlister.html')

@app.route('/searcherpage')
def searchpage():
    return render_template('searcher.html')

@app.route('/registerpage')
def registerpage():
    return render_template('register.html')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/register',methods=['POST','GET'])
def register():
    data = request.get_json()
    if (data['username'] == ""):
        return jsonify({"data":"fail"})
    if(data['username'] in database):
        return jsonify({"data":"already"})
    else:
        database.append(data['username'])
        return jsonify({"data":"success"})
    
@app.route('/login',methods=['POST','GET'])
def login():
    data = request.get_json()
    if(data['username'] in database):
        access_token = create_access_token(identity=data['username'])
        response = make_response(jsonify({"data":"success","redirect":"/playlisterpage"}))
        set_access_cookies(response,access_token)
        return response
    else:
        return jsonify({"data":"fail"})


#PLAYLIST ADDER
@app.route('/playlistadder',methods=['GET','POST'])
@jwt_required()
def playlistadder():
    
    data = request.get_json()
    username = get_jwt_identity()
    if username not in playlist:
        playlist[username]=[]
    if data['audioid'] not in playlist[username]:
        playlist[username].append(data['audioid'])
        return jsonify({'data':'success'})
    else:
        return jsonify({'data':'already'})

@app.route('/playlistgetter',methods=['GET','POST'])
@jwt_required()
def playlistgetter():
    data = get_jwt_identity()
    if data not in database:
        return jsonify({'data':'nouser'})
    if data not in playlist:
        return jsonify({'data':'noplay'})
    details = {}
    for i in playlist[data]:
        details[i]=songdetails[i]
    return jsonify(details)




#ROUTERS
@app.route('/downloader',methods=['GET','POST'])
@jwt_required()
def downloader():
    username = get_jwt_identity()
    data = request.get_json()
    if (username == ""):
        return jsonify({"data":"fail"})
    match = re.search(r'(?<=watch\?v=)[\w-]{11}', data['url'])
    if match == "":
        return jsonify({"data":"fail"})
    try:
        if match[0] in songdetails:
            temp = match[0]
            return jsonify({"data":"success",'audiosrc':songdetails[temp][2],'videosrc':songdetails[temp][1],'audiotittle':songdetails[temp][0],'audioid':match[0]})
    except Exception as e:
        print(e)

    if(username in database):
        res = audiodownloader(data['url'])
        if res == "err":
            return jsonify({"data":"Invalid Url"})
        else:
            songdetails[res[3]]=[res[0],res[1],res[2]]
            return jsonify({"data":"success",'audiosrc':'static/audios/'+res[2],'videosrc':res[1],'audiotittle':res[0],'audioid':res[3]})
    else:
        return jsonify({"data":"fail"})
    
def audiodownloader(url):
    with yt_dlp.YoutubeDL(ytlopts) as ydl:
        try:
            audiosrc=""
            info = ydl.extract_info(url,download=True)
            tittle = info["title"]
            thumbnail = info["thumbnail"]
            temp = info['formats']
            audioid=info["id"]
            for i in range(len(temp)):
                if(temp[i]['audio_ext']!="none" and temp[i]['audio_ext']=="webm"):
                    audiosrc=info["id"]+"."+temp[i]['audio_ext']
            return tittle,thumbnail,audiosrc,audioid
        except Exception as e:
            return "err"


@app.route('/searcher',methods=['GET','POST'])
def searcher():
    res = request.get_json()
    if(res['searchid']!=""):
        searchid = res['searchid']
        searchid = searchid.replace(" ", "+")
        searchid = "https://www.youtube.com/results?search_query="+searchid
        data = urllib.request.urlopen(searchid)
        data = data.read().decode()
        videoid = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', data)  
        videoid = list(OrderedDict.fromkeys(videoid))
        if videoid:
            return jsonify({"data":videoid})
        else:
            return jsonify({"data":'fail'})
    else:
        return jsonify({"data":'fail'}) 



if __name__ == "__main__":
    app.run(debug=True)
