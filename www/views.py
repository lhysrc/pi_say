# coding=utf-8
from main import baidu_tts,ne_music,play_sound
from www import app
from flask import make_response
import threading,time

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

import main.tell_time
@app.route('/time')
def tell_time():
    t = main.tell_time.tell_time()
    return str(t)

import urllib
@app.route('/tts/<name>')
def tts_page(name):
    text = urllib.quote_plus(name.encode('utf8'))
    threading.Thread(target=baidu_tts.read_aloud,args=(text,False,5,5,9,3)).start()
    return name


@app.route('/lcsong/<int:n>')
def play_local_song(n):
    baidu_tts.read_aloud("准备播放本地音乐。",True)
    threading.Thread(target=play_sound.play_local_music,args=(1,)).start()
    return '开始播放%d首本地歌曲' % n

@app.route('/rdsong/<id>')
def play_rd_song(id):
    baidu_tts.read_aloud("准备随机播放音乐。",True)
    url = 'http://music.163.com/#/discover/toplist?id=%s'%id
    threading.Thread(target=ne_music.play_a_list,args=(url,1)).start()
    return '开始随机播放音乐'

@app.route('/ltsong/<id>')
def play_a_list(id,n=10):
    baidu_tts.read_aloud("准备播放%d首音乐。"%n,True)
    url = 'http://music.163.com/#/discover/toplist?id=%s'%id
    threading.Thread(target=ne_music.play_a_list,args=(url,n)).start()
    return 'ok'

# @app.route('/tts',methods='post')
# def tts():
#     baidu_tts.read_aloud("123")