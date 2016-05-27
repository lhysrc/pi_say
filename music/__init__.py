# coding=utf-8
import logging
import os
import random,threading

from common import util
from .ne_music import neteaseMusic
from .song_info import SongInfo
from .xm_music import xiami
from .player import Player

log = logging.getLogger(__name__)

net_lock = threading.Lock() #加载音乐信息的锁
player = Player()
def play_songs(url='./music_files', n=1, rdm=True, vol=None):
    """
        n:播放n首
        rdm:是否随机
    """
    if isinstance(url,unicode):url = url.encode('utf-8')
    infos = []
    with net_lock:
        if 'music.163.com' in url:
            x = neteaseMusic(url)
            for s in x.song_infos:
                si = SongInfo(s['durl'],s['song_name'],s['artist_name'])
                si.song_page = s['song_url']
                si.song_type = 'ne'
                infos.append(si)
        elif 'xiami.com' in url: # todo 虾米信息加载未完善
            x = xiami()
            x.url_parser([url])
            infos = x.song_infos
        else:
            files = util.get_files_from_path(url,'.mp3')
            infos = [SongInfo(f,file_name=os.path.split(f)[1].decode('utf-8'),is_local=True) for f in files]
            pass
    # n = len(x.song_infos) if n<=0 or n>len(x.song_infos) else n
    # l = random.sample(x.song_infos,n) if rdm else x.song_infos[:n]
    if rdm: random.shuffle(infos)
    infos = filter(lambda i:i.url,infos)[:n]
    if vol:
        player.playing_volume = vol
    if not player.playing_flag:
        player.playing_idx = 0
        player.songs = infos
        player.recall()
    else:
        # 如果正在播放，把新获取的歌曲加到列表后
        player.songs += infos

    # for i in infos[:n]:
    #     if not i.url:
    #         log.warn(u"地址‘ %s ’无法播放，将跳过。"%i.url)
    #         continue
    #     log.info(u"播放%s。 %s" % (i.file_name,i.song_page)) # http://music.163.com/song/%s
    #     play_sound.play_music(i.url)

def is_loading_song_infos():
    return net_lock.locked()
#
# def is_playing():
#     return player.playing_flag
#
# def set_vol(vol):
#     player.set_volume(vol)
#
# def play_and_pause():
#     player.play_and_pause()
#
# def next_song():
#     player.next()
#
# def stop():
#     player.stop()
