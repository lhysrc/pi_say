# coding=utf-8
import logging
import os
import random,threading

from common import util
from main import play_sound
from music.ne_music import neteaseMusic
from music.xm_music import xiami

log = logging.getLogger(__name__)

net_lock = threading.Lock() #加载音乐信息的锁
def play_songs(url='./music_files', n=1, rdm=True):
    """
        n:播放n首
        rdm:是否随机
    """
    with net_lock:
        if 'music.163.com' in url:
            x = neteaseMusic(url)
            infos = x.song_infos
        elif 'xiami' in url: # todo 虾米信息加载未完善
            x = xiami()
            x.url_parser([url])
            infos = None
        else:
            files = util.get_files_from_path(url,'.mp3')
            infos = [SongInfo(f,file_name=os.path.split(f)[1],is_local=True) for f in files]
            pass
    # n = len(x.song_infos) if n<=0 or n>len(x.song_infos) else n
    # l = random.sample(x.song_infos,n) if rdm else x.song_infos[:n]

    if rdm: random.shuffle(infos)
    for i in infos[:n]:
        if not i.url:
            log.warn(u"地址‘ %s ’无法播放，将跳过。"%i.url)
            continue
        log.info(u"播放%s。 %s" % (i.file_name,i.song_page)) # http://music.163.com/song/%s
        play_sound.play_music(i.url)

def is_loading_song_infos():
    return net_lock.locked()
