# coding=utf-8
import threading

from flask import render_template,make_response,request

from main import baidu_tts,ne_music,play_sound
from www import app
from common import util

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html',index='index')

@app.route('/log',methods=['get'])
@app.route('/log/<int:page_idx>', methods=['get'])
def page_log(page_idx=None):
    if not page_idx:file_name = "./log/log"
    else:
        logs = util.GetFileFromThisRootDir("./log")
        logs.sort()
        if page_idx>=len(logs):return page_not_found(0)
        file_name = logs[page_idx]
    with open(file_name,'r+') as f:
        log_text = f.read()
    ret = {
        'log':'log',
        'file_name':file_name,
        'log_text':unicode(log_text,'utf-8'),
        'next': page_idx+1 if page_idx else 1
    }
    return render_template('log.html', **ret)


@app.route('/read',methods=['get'])
def page_read():
    return render_template('read.html',read='read')

'''
/read isn't multithreading
/tts is multithreading to tts
'''

@app.route('/read',methods=['post'])
def tts():
    json_data = {key:dict(request.form)[key][0] for key in dict(request.form)}
    # text = json_data['text']
    # print(json_data)
    app.logger.info(u"获得播报信息：%s" % json_data['text'])
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
@app.route('/time',methods=['get'])
def tell_time1():
    t = main.tell_time.tell_time()
    return str(t)

import main.tell_time
@app.route('/time',methods=['post'])
def tell_time2():
    json_data = {key:dict(request.form)[key][0] for key in dict(request.form)}
    json_data['text'] = main.tell_time.get_strtime()
    json_data['text'] = urllib.quote_plus(json_data['text'])
    baidu_tts.read_aloud(**json_data)
    return json_data['text']

import main.weather
@app.route('/weather',methods=['get','post'])
def tell_weather():
    json_data = {key:dict(request.form)[key][0] for key in dict(request.form)}
    json_data['text'] = main.weather.tell_today()
    json_data['text'] = urllib.quote_plus(json_data['text'])
    baidu_tts.read_aloud(**json_data)
    return json_data['text']

import urllib
@app.route('/tts/<name>',methods=['get'])
def tts_page_1(name):
    text = urllib.quote_plus(name.encode('utf8'))
    threading.Thread(target=baidu_tts.read_aloud,args=(text,False,5,5,9,3)).start()
    return name


@app.route('/tts',methods=['post'])
def tts_page_2():
    json_data = {key:dict(request.form)[key][0] for key in dict(request.form)}
    app.logger.info(u"获得播报信息：%s" % json_data['text'])
    name = json_data['text']
    text = urllib.quote_plus(name.encode('utf8'))
    threading.Thread(target=baidu_tts.read_aloud,args=(text,False,5,5,9,3)).start()
    return text

@app.route('/lcsong',methods=['get','post'])
def play_local_song():
    p = check_is_playing()
    if p: return p,204
    json_data = {key:dict(request.form)[key][0] for key in dict(request.form)}
    path = json_data['path']
    n = int(json_data['cnt'])
    baidu_tts.read_aloud("准备播放本地音乐",True)
    threading.Thread(target=play_sound.play_local_music,args=(n,path)).start()
    return '',200
    # p = check_is_playing()
    # if p: return p,204
    # baidu_tts.read_aloud("准备播放本地音乐",True)
    # threading.Thread(target=play_sound.play_local_music,args=(n,)).start()
    # return '',200

@app.route('/rdsong/<id>')
def play_rd_song(id):
    p = check_is_playing()
    if p: return p,204
    baidu_tts.read_aloud("准备随机播放音乐",True)
    url = 'http://music.163.com/#/discover/toplist?id=%s'%id
    threading.Thread(target=ne_music.play_a_list,args=(url,1)).start()
    return '开始随机播放音乐'

@app.route('/ltsong/<id>')
def play_a_list(id,n=10):
    p = check_is_playing()
    if p: return p,204
    baidu_tts.read_aloud("准备播放%d首音乐"%n,True)
    url = 'http://music.163.com/#/discover/toplist?id=%s'%id
    threading.Thread(target=ne_music.play_a_list,args=(url,n)).start()
    return '',200

@app.route('/play_url',methods=['post'])
def play_url():
    p = check_is_playing()
    if p: return p,204
    json_data = {key:dict(request.form)[key][0] for key in dict(request.form)}
    url = json_data['url']
    n = int(json_data['cnt'])
    rdm = json_data['rdm']
    threading.Thread(target=ne_music.play_a_list,args=(url,n,rdm=='true')).start()
    return '',200

def check_is_playing():
    if ne_music.loading_url():
        return '当前正在加载音乐信息，已准备播放'
    if play_sound.is_playing_music():
        return '当前正在播放音乐'
    return ""

# @app.route('/tts',methods='post')
# def tts():
#     baidu_tts.read_aloud("123")