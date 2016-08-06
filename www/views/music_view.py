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
    if 'vol' in json_data:
        player.set_volume(json_data['vol'])
    player.emit_playing_info()
    return '',200

import random
@app.route('/playing-info')
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

from music.ne_api import NetEase
ne = NetEase()
@app.route('/ne-api/<string:type>')
def ne_api_route(type):
    if type == 'playlists':
        pls = ne.top_playlists()
        if pls:
            pls = map(lambda pl:{'id':pl['id'],'name':pl['name'],},pls)
            pls = random.sample(pls,10)
            return jsonify(pls)
        else:
            return "",200
    else:
        return "",200