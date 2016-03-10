# coding=utf-8
from main import baidu_tts,ne_music
from www import app
import threading

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


@app.route('/rdsong/<id>')
def play_rd_song(id):
    baidu_tts.read_aloud("准备随机播放音乐。",True)
    url = 'http://music.163.com/#/discover/toplist?id=%s'%id
    threading.Thread(target=ne_music.play_a_random_song,args=(url,)).start()
    return 'ok'

@app.route('/ltsong/<id>')
def play_a_list(id,n=10):
    baidu_tts.read_aloud("准备播放%d首音乐。"%n,True)
    url = 'http://music.163.com/#/discover/toplist?id=%s'%id
    threading.Thread(target=ne_music.play_a_list,args=(url,n)).start()
    return 'ok'

# @app.route('/tts',methods='post')
# def tts():
#     baidu_tts.read_aloud("123")