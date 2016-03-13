# coding=utf-8
from main import baidu_tts,ne_music,play_sound
from www import app
from flask import render_template,make_response,request,jsonify
import threading,time

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html',index='index')

@app.route('/read',methods=['get'])
def page_read():
    return render_template('read.html',read='read')

@app.route('/read',methods=['post'])
def tts():
    json_data = {key:dict(request.form)[key][0] for key in dict(request.form)}
    # text = json_data['text']
    # print(json_data)
    app.logger.info(u"获得准备播报的数据：%s" % json_data['text'])
    json_data['text'] = urllib.quote_plus(json_data['text'].encode('utf8'))
    baidu_tts.read_aloud(**json_data)
    #threading.Thread(target=baidu_tts.read_aloud, args=(json_data)).start()
    return render_template('read.html',read='read')

@app.route('/music')
def page_music():
    return render_template('music.html',music='music')

@app.route('/test')
def test():
    return make_response('test',200)
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

import main.weather
@app.route('/weather')
def tell_weather():
    w = main.weather.tell_today()
    baidu_tts.read_aloud(main.baidu_tts.read_aloud(w))
    return w

import urllib
@app.route('/tts/<name>')
def tts_page(name):
    text = urllib.quote_plus(name.encode('utf8'))
    threading.Thread(target=baidu_tts.read_aloud,args=(text,False,5,5,9,3)).start()
    return name


@app.route('/lcsong/<int:n>')
def play_local_song(n):
    baidu_tts.read_aloud("准备播放本地音乐",True)
    threading.Thread(target=play_sound.play_local_music,args=(1,)).start()
    return '开始播放%d首本地歌曲' % n

@app.route('/rdsong/<id>')
def play_rd_song(id):
    baidu_tts.read_aloud("准备随机播放音乐",True)
    url = 'http://music.163.com/#/discover/toplist?id=%s'%id
    threading.Thread(target=ne_music.play_a_list,args=(url,1)).start()
    return '开始随机播放音乐'

@app.route('/ltsong/<id>')
def play_a_list(id,n=10):
    baidu_tts.read_aloud("准备播放%d首音乐"%n,True)
    url = 'http://music.163.com/#/discover/toplist?id=%s'%id
    threading.Thread(target=ne_music.play_a_list,args=(url,n)).start()
    return 'ok'

# @app.route('/tts',methods='post')
# def tts():
#     baidu_tts.read_aloud("123")