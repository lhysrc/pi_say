from main import baidu_tts
from www import app


@app.route('/')
def index():
    return "Hello, World!"

# @app.route('/wx', methods = ['GET', 'POST'] )
# def wx():
#     from WeiXinCore.WeiXin import check_signature,echo
#     from flask import request
#     if not check_signature(request.args) and not app.debug:
#         return ""
#     return echo

import urllib
@app.route('/tts/<name>')
def tts_page(name):
    baidu_tts.read_aloud(urllib.quote_plus(name.encode('utf8')),per=3)
    return name

# @app.route('/tts',methods='post')
# def tts():
#     baidu_tts.read_aloud("123")