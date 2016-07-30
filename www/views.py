# coding=utf-8
import threading

from flask import render_template,make_response,request,jsonify

from common import util
from main import baidu_tts, play_sound
# from music import ne_music
from www import app

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
        logs = util.get_files_from_path("./log")
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

@app.route('/config',methods=['get'])
def page_config():
    ret = {
        'cfg': True,
        '_581': gz_bus.get_pause_day('581') == 0,
        '_498': gz_bus.get_pause_day('498') == 0,
    }
    return render_template('config.html',**ret)


@app.route('/bus_status',methods=['post'])
def bus_status():
    # json_data = {key: dict(request.form)[key][0] for key in dict(request.form)}
    # bus = json_data['bus']
    # days = json_data['days']
    # gz_bus.pause_tell_bus(bus,days)
    ret = {
        '581':gz_bus.get_pause_day('581'),
        'b11': gz_bus.get_pause_day('b11'),
        '498': gz_bus.get_pause_day('498'),
    }
    return  jsonify(ret)
from main import gz_bus
@app.route('/pause-bus',methods=['post'])
def pause_tell_bus():
    json_data = {key: dict(request.form)[key][0] for key in dict(request.form)}
    bus = json_data['bus']
    days = json_data['days']
    gz_bus.pause_tell_bus(bus,days)
    return ""


import json
@app.route('/read',methods=['post'])
def tts():
    # print request.data
    json_data = json.loads(request.data) #{key:dict(request.form)[key][0] for key in dict(request.form)}
    # text = json_data['text']
    # print(json_data)
    app.logger.info(u"获得播报信息：%s" % json_data['text'])
    if 'delay_sec' in json_data and json_data['text'] == u'定时时间到':
        json_data['cache'] = True
    json_data['text'] = urllib.quote_plus(json_data['text'].encode('utf8'))
    baidu_tts.read_aloud_async(**json_data)
    #threading.Thread(target=baidu_tts.read_aloud, args=(json_data)).start()
    return u'将在%s后播报。'%json_data['delay_sec'] if 'delay_sec' in json_data else ''

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
    json_data['idx'] = 0 if 'idx' not in json_data else json_data['idx']
    json_data['text'] = main.weather.day_of_week(int(json_data['idx']))
    del json_data['idx']
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

# @app.route('/lcsong',methods=['get','post'])
# def play_local_song():
#     p = check_is_playing()
#     if p: return p
#     json_data = {key:dict(request.form)[key][0] for key in dict(request.form)}
#     path = str(json_data['url'])
#     n = int(json_data['cnt'])
#     app.logger.info(u"准备播放%d首'%s'里的音乐。"%(n,path))
#     # baidu_tts.read_aloud("准备播放本地音乐",True)
#     # threading.Thread(target=play_sound.play_local_music,args=(n,path)).start()
#     threading.Thread(target=music.play_songs, args=(path, n, True)).start()
#     return '',200
#     # p = check_is_playing()
#     # if p: return p,204
#     # baidu_tts.read_aloud("准备播放本地音乐",True)
#     # threading.Thread(target=play_sound.play_local_music,args=(n,)).start()
#     # return '',200

# @app.route('/rdsong/<id>')
# def play_rd_song(id):
#     p = check_is_playing()
#     if p: return p
#     baidu_tts.read_aloud("准备随机播放音乐",True)
#     url = 'http://music.163.com/#/discover/toplist?id=%s'%id
#     threading.Thread(target=ne_music.play_a_list, args=(url, 1)).start()
#     return '开始随机播放音乐'
#
# @app.route('/ltsong/<id>')
# def play_a_list(id,n=10):
#     p = check_is_playing()
#     if p: return p
#     baidu_tts.read_aloud("准备播放%d首音乐"%n,True)
#     url = 'http://music.163.com/#/discover/toplist?id=%s'%id
#     threading.Thread(target=ne_music.play_a_list, args=(url, n)).start()
#     return '',200

import music
@app.route('/play_url',methods=['post'])
def play_url():
    p = check_is_playing()
    if p: return p
    json_data = json.loads(request.data)  # {key:dict(request.form)[key][0] for key in dict(request.form)}
    url = json_data['url']
    n = int(json_data['cnt'])
    rdm = json_data['rdm']
    app.logger.info(u"准备播放%d首'%s'里的音乐。" % (n, url))
    # threading.Thread(target=ne_music.play_a_list, args=(url, n, rdm == 'true')).start()
    threading.Thread(target=music.play_songs, args=(url, n, rdm)).start()
    return '',200


from music import player
player_func = {
    'stop':player.stop,
    'p':player.play_and_pause,
    'next':player.next,
    'prev': player.prev,
}
@app.route('/set-player',methods=['post'])
def set_player():
    json_data = json.loads(request.data)
    if 'func' in json_data and json_data['func'] in player_func:
        player_func[json_data['func']]()
    if 'vol' in json_data:
        player.set_volume(json_data['vol'])
    return '',200

import random
@app.route('/playing-info',methods=['post'])
def get_playing_info():
    ret = {
        'song_name':player.get_playing_song().file_name if player.playing_flag else None,
        'vol':player.playing_volume,
        'pause':player.pause_flag,
        'playing':player.playing_flag
    }
    # ret = {
    #     'song_name': music.SongInfo('url','name','artist').file_name,
    #     'vol'      : random.randint(0,100),
    #     'pause'    : True,
    #     'playing'  : True
    # }
    return jsonify(ret)

def check_is_playing():
    if music.is_loading_song_infos():
        return '当前正在加载音乐信息，已准备播放！'
    if player.playing_flag:
        return '当前正在播放音乐。'
    return ""

from main import task2
@app.route('/tasks',methods=['get','post'])
@app.route('/tasks/<type>',methods=['get'])
def cfg_tasks(type = None):
    # tasks = task2.tasks
    if request.method == 'GET':
        tks = map(lambda t:t.to_dict(True),task2.tasks)
        tks = filter(lambda t:t != None,tks)
        if type : tks = filter(lambda t:t['type']==type,tks)
        return jsonify(result=tks)
    if request.method == 'POST':
        rq_data = json.loads(request.data)
        #for tk in rq_data:
        if not isinstance(rq_data,list):rq_data = [rq_data]
        for tk_dic in rq_data:
            if 'id' in tk_dic:
                task2.tasks = [task2.Task(**tk_dic) if tk.id == tk_dic['id'] else tk for tk in task2.tasks]
                # for i,tk in enumerate(tasks):
                #     if tk.id == tk_dic['id']:
                #         tasks[i] = task2.Task(**tk_dic)
            else:
                task2.tasks.append(task2.Task(**tk_dic))
        task2.save_all_tasks()
        return '',200

@app.route('/bus',methods=['get','post'])
@app.route('/bus/<int:search_id>',methods=['get'])
def bus_tell_status(search_id=None):
    if request.method == 'GET':
        if search_id:
            if search_id in gz_bus.status:
                return jsonify(result=gz_bus.status[search_id])
            else:
                return jsonify(result=False)
        else:
            return jsonify(result=gz_bus.status)
    if request.method == 'POST':
        rq_data = json.loads(request.data)
        #if rq_data['id'] in gz_bus.status:
        if rq_data['status']:
            threading.Thread(target=gz_bus.tell_bus, args=(rq_data['bus_name'],rq_data['station'],rq_data['id'])).start()
        else:
            if rq_data['id'] in gz_bus.status:
                gz_bus.status[rq_data['id']] = False
        return '',200
        # else:
        #     return '该报站任务未执行。',200
# @app.route('/tts',methods='post')
# def tts():
#     baidu_tts.read_aloud("123")


