from flask import Blueprint
import yt_dlp

from flask import request,jsonify,make_response

import urllib.request

from collections import OrderedDict

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager,set_access_cookies,unset_jwt_cookies


from packages import sqliteconn

from controller import playlistcont

import re


songdetails = {}
playlist = {}


ytlopts={
    'format':'bestaudio/best',
    'outtmpl':'static/audios/%(id)s.%(ext)s',
}

api_bp = Blueprint("apis",__name__)



@api_bp.route('/rmsong',methods=['POST'])
@jwt_required()
def rmsong():

    try:
        data = request.get_json()
        username = get_jwt_identity()
        
        playlistcont.song_remover(data,username)

        return jsonify({"data":"success"})

    except Exception as e:
        print("Error is ",e)
        return jsonify({
            "status":500,  
            "data":"Internal Server Error"
        },500)




@api_bp.route('/testlist',methods=['GET'])
def testlist():
    try:
        return jsonify(songdetails)
    except Exception as e:
        print("Error is ",e)
        return jsonify({
            "status":500,  
            "data":"Internal Server Error"
        },500)


@api_bp.route('/register',methods=['POST','GET'])
def register():
    try:
        data = request.get_json()

        sqlitecon = sqliteconn.initconn()

        sqcursor = sqlitecon.cursor()

        res = sqlitecon.execute("SELECT COUNT(*) from tbl_users WHERE username = ?",(data["username"],))

        if (data['username'] == ""):
            return jsonify({"data":"fail"})

        if(res.fetchall()[0][0])>0:
            return jsonify({"data":"already"})
        else:
            sqcursor.execute("INSERT into tbl_users (username) VALUES (?)", (data["username"],))
            return jsonify({"data":"success"})
    except Exception as e:
        print("Error is ",e)
        return jsonify({
            "status":500,  
            "data":"Internal Server Error"
        },500)


    finally:
        sqlitecon.commit()
        sqcursor.close()
        sqlitecon.close()

    
@api_bp.route('/login',methods=['POST','GET'])
def login():
    try:

        data = request.get_json()

        sqlitecon = sqliteconn.initconn()

        sqcursor = sqlitecon.cursor()

        res = sqlitecon.execute("SELECT COUNT(*) from tbl_users WHERE username = ?",(data["username"],))

        if(res.fetchall()[0][0])>0:
            access_token = create_access_token(identity=data['username'])
            response = make_response(jsonify({"data":"success","redirect":"/playlister"}))
            set_access_cookies(response,access_token)
            return response
        else:
            return jsonify({"data":"fail"})
            

    except Exception as e:
        print("Error is ",e)
        return jsonify({
            "status":500,  
            "data":"Internal Server Error"
        },500)

    finally:
        sqlitecon.commit()
        sqcursor.close()
        sqlitecon.close()


@api_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():

    response = jsonify({
        "status":200,
        "data":"/"
    })

    unset_jwt_cookies(response)

    return response

#PLAYLIST ADDER
@api_bp.route('/playlistadder',methods=['GET','POST'])
@jwt_required()
def playlistadder():

    try:
    
        data = request.get_json()
        username = get_jwt_identity()


        sqlitecon = sqliteconn.initconn()

        sqcursor = sqlitecon.cursor()

        res = sqcursor.execute("SELECT COUNT(*) FROM tbl_userongs WHERE username = ? AND songid = ?",(username,data['audioid'],))
        
        res_data = res.fetchall()

        print(res_data)

        if(len(res_data))>0:
            sqcursor.execute("INSERT into tbl_userongs (username,songid) VALUES (?,?)", (username,data['audioid'],))
            return jsonify({'data':'success'})
        else:
            return jsonify({'data':'already'})
        
        # if username not in playlist:
        #     playlist[username]=[]
        # if data['audioid'] not in playlist[username]:
        #     playlist[username].append(data['audioid'])
        #     return jsonify({'data':'success'})
        # else:
        #     return jsonify({'data':'already'})

    except Exception as e:
        print("Error is ",e)
        return jsonify({
            "status":500,  
            "data":"Internal Server Error"
        },500)

    finally:
        sqlitecon.commit()
        sqcursor.close()
        sqlitecon.close()

@api_bp.route('/playlistgetter',methods=['GET'])
@jwt_required()
def playlistgetter():
    data = get_jwt_identity()

    sqlitecon = sqliteconn.initconn()

    sqcursor = sqlitecon.cursor()


    res = sqcursor.execute("SELECT songid FROM tbl_userongs WHERE username = ? AND status = 0",(data,))
    
    # if data not in database:
    #     return jsonify({'data':'nouser'})

    res_data = res.fetchall()
    print(res_data)
    if len(res_data)<1:
        return jsonify({'data':'noplay'})


    details = {}
    ids = [x[0] for x in res_data]

    placeholders = ",".join(["?"] * len(ids))

    query = f"""
    SELECT *
    FROM tbl_songs
    WHERE songid IN ({placeholders})
    """

    sqcursor.execute(query, ids)

    rows = sqcursor.fetchall()

    for i in rows:
        print(i)
        details[i[1]]=[i[2],i[4],i[3],i[5]]

    # for i in playlist[data]:
    #     details[i]=songdetails[i]
    return jsonify(details)

#ROUTERS
@api_bp.route('/downloader',methods=['GET','POST'])
@jwt_required()
def downloader():

    try:
        username = get_jwt_identity()
        data = request.get_json()

        sqlitecon = sqliteconn.initconn()

        sqcursor = sqlitecon.cursor()


        if (username == ""):
            return jsonify({"data":"fail"})
        match = re.search(r'(?<=watch\?v=)[\w-]{11}', data['url'])
        if match == "":
            return jsonify({"data":"fail"})
        try:

            res = sqcursor.execute("SELECT * FROM tbl_songs WHERE songid = ?",(match[0],))
            print(res)
            if match[0] in songdetails:
                temp = match[0]
                return jsonify({"data":"success",'audiosrc':songdetails[temp][2],'videosrc':songdetails[temp][1],'audiotittle':songdetails[temp][0],'audioid':match[0]})
        except Exception as e:
            print(e)
        # if(username in database):
        res = audiodownloader(data['url'])
        if res == "err":
            return jsonify({"data":"Invalid Url"})
        else:

            sqcursor.execute("INSERT into tbl_songs (songid,tittle,audiosrc,videosrc,duration) VALUES (?,?,?,?,?)", (res[3],res[0],res[2],res[1],res[4],))
            # songdetails[res[3]]=[res[0],res[1],res[2]]
            return jsonify({"data":"success",'audiosrc':'static/audios/'+res[2],'videosrc':res[1],'audiotittle':res[0],'audioid':res[3]})
        # else:
        #     return jsonify({"data":"fail"})
    
    except Exception as e:
        print("Error is ",e)
        return jsonify({
            "status":500,  
            "data":"Internal Server Error"
        },500)

    finally:
        sqlitecon.commit()
        sqcursor.close()
        sqlitecon.close()
    
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

            duration = info["duration"]
            return tittle,thumbnail,audiosrc,audioid,duration
        except Exception as e:
            print("Error is ",e)
            return "err"


@api_bp.route('/searcher',methods=['GET','POST'])
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