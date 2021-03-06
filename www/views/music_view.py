# coding=utf-8
import threading

from flask import render_template,make_response,request,jsonify
import json
# from common import util
# from main import baidu_tts, play_sound
# from music import ne_music
from www import app


@app.route('/music')
def page_music():
    return render_template('music.html',music='music')



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
        if json_data['func'] in ['p','stop']:    # 暂停和停止需要emit，未调用recall
            player.emit_playing_info()
    elif 'vol' in json_data:
        player.set_volume(json_data['vol'])
        player.emit_playing_info() # player.recall里已有emit，所以为func不需要emit
    return '',200


@app.route('/playing-info')
def get_playing_info():
    # ret = {
    #     'song_name':player.get_playing_song().file_name if player.playing_flag else None,
    #     'vol':player.playing_volume,
    #     'pause':player.pause_flag,
    #     'playing':player.playing_flag
    # }
    ret = player.playing_info
    return jsonify(ret)

def check_is_playing():
    if music.is_loading_song_infos():
        return '当前正在加载音乐信息，已准备播放！'
    if player.playing_flag:
        return '当前正在播放音乐。'
    return ""

from music.ne_api import NetEase
from random import sample
from datetime import datetime
ne = NetEase()
pls_t = {
    "time":datetime.now(),
    "pls":ne.top_playlists(limit=100)
}

pls_num = 10 #要显示的歌单数目
@app.route('/ne-api/<string:type>')
def ne_api_route(type):
    if type == 'playlists':
        if (datetime.now() - pls_t["time"]).seconds > (60*60*6):    # 六小时刷新歌单
            pls_t["pls"] = ne.top_playlists(limit=100)
            pls_t["time"] = datetime.now()
            app.logger.info(u"已重新获取100首歌单列表。")
        pls = pls_t["pls"][:]
        if not pls:
            return "",200

        cnpls = filter(lambda pl: u"华语" in pl["tags"], pls)
        yypls = filter(lambda pl: pl not in cnpls and u"粤语" in pl["tags"] , pls)
        qtpls = filter(lambda pl: pl not in cnpls and pl not in yypls, pls)

        # 筛选歌曲，华语5个，粤语2个，其他3个
        cn_num = min(5,len(cnpls))
        yy_num = min(2,len(yypls))
        qt_num = pls_num - cn_num - yy_num

        retpls = sample(cnpls,cn_num) + sample(yypls,yy_num) + sample(qtpls,qt_num)

        retpls = map(lambda pl: {'id': pl['id'], 'name': pl['name'],}, retpls)
        return jsonify({'pls': retpls})





    else:
        return "",200
