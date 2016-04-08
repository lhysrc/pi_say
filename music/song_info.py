# coding=utf-8
class SongInfo(object):
    song_type = ''
    song_page = '' # 音乐页面
    def __init__(self,url,song_name=None,artist=None,file_name=None,is_local=False):
        self.url = url
        self.song_name = song_name
        self.artist = artist
        self._file_name = file_name
        self.is_local = is_local


    @property
    def file_name(self):
        if self._file_name:
            return self._file_name
        return "{0}-{1}.mp3".format(self.song_name,self.artist)
