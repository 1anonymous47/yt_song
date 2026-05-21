from flask import Flask,redirect,url_for

from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes.webpages import web_bp
from routes.apiendpoints import api_bp

from packages import sqliteconn
import sys

from datetime import timedelta

#------------- Initiation
if(sqliteconn.initdb()):
    print("SQ LITE DB Connected")
else:
    print("Failed")
    sys.exit(1)



app = Flask(__name__)

app.register_blueprint(web_bp)
app.register_blueprint(api_bp,url_prefix="/api")

app.config["JWT_SECRET_KEY"] = "yt_player"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=3650)

jwt = JWTManager(app)


@jwt.unauthorized_loader
def missing_token_callback(reason):
    return redirect("/")

@jwt.expired_token_loader
def expired_token_callback(wt_header, jwt_payload):
    return redirect("/")

CORS(app)
            


# @app.route('/writer')
# def writer():
#     f = open("songdetails.txt",'w')
#     f.write(str(songdetails))
#     f = open("playlist.txt",'w')
#     f.write(str(playlist))
#     f = open("database.txt",'w')
#     f.write(str(database))
#     print(songdetails)
#     print()
#     print(playlist)
#     print()
#     print(database)
#     return "Writed"

# @app.route('/reader')
# def reader():
#     f = open("songdetails.txt",'r')
#     songdetails = f.read
#     print(songdetails)
#     f = open("playlist.txt",'r')
#     playlist = f.read()
#     f = open("database.txt",'r')
#     database = f.read()
#     print(songdetails)
#     print()
#     print(playlist)
#     print()
#     print(database)
#     return "Readed"







if __name__ == "__main__":
    app.run(debug=True)
