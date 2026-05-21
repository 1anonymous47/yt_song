from flask import Blueprint
from flask import render_template


from flask_jwt_extended import jwt_required


web_bp = Blueprint("webs",__name__)


# @web_bp.route('/test')
# def printer():
#     return jsonify({"Songdetails":songdetails,"Playlists":playlist})

#WEBPAAGES
@web_bp.route('/downloader')
@jwt_required()
def downloaderpage():
    return render_template('downloader.html')

@web_bp.route('/playlister')
@jwt_required()
def playlisterpage():
    return render_template('playlister.html')

@web_bp.route('/searcher')
@jwt_required()
def searchpage():
    return render_template('searcher.html')

@web_bp.route('/register')
def registerpage():
    return render_template('register.html')

@web_bp.route('/')
def loginpage():
    return render_template('login.html')

# @web_bp.route('/test')

# def test():
#     return render_template('test.html')