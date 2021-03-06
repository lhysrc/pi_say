# coding=utf-8
# 播放本地音乐
# 播放网络音乐
# 报站
# 播报语音：天气
# 自动签到（无需自定义）
import json

import baidu_tts
import config
import gz_bus
# import play_sound
import weather
import music

# task_names = {
#     "播放本地音乐":play_sound.play_local_music,
#     "播放网络音乐":ne_music.play_a_list,
#     "报站":gz_bus.baozhan,
#     "播报天气":0,
#     "播报语音":baidu_tts.read_aloud,
# }
# class Enum(set):
#     def __getattr__(self, item):
#         if item in self:return item
#         else:raise AttributeError
#     def add(self, *args, **kwargs):
#         pass
#
# TaskName = Enum({"baozhan","只"})


# import datetime
from common import util
from main import tell_time
from log import log


class Task(object):
    # name = ""
    # func = None
    # args = ()
    # t_hour = 0
    # t_min = 0
    # type = 3 # 1 工作日，2 假日
    def __init__(self,name,hr,mn,func,args=(),type=3,pause_days=0):
        self.name = name
        self.func = func
        self.args = args
        self.t_hour = hr
        self.t_min = mn
        self.type = type    # 1 工作日，2 假日
        self.pause_days = pause_days

    def __repr__(self):
        return "%s('%s',%s,%s,%s,%s,%s,%s) " % (
        self.__class__.__name__, self.name,self.t_hour, self.t_min, self.func.__name__, self.args, self.type, self.pause_days)

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else: return None

    def __setitem__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            return
    def to_dict(self):
        d = self.__dict__.copy()
        del d['func']
        return d

    #     self._start_date = datetime.datetime.today()
    # @property
    # def pause_days(self):
    #     if not self._reset_time: return 0
    #     return (datetime.datetime.today() - self._reset_time).days
    # @pause_days.setter
    # def pause_days(self,value):
    #     if not isinstance(value, int):
    #         raise ValueError('score must be an integer!')
    #     if value < 0: self._reset_time = None
    #     else:
    #         self._reset_time = datetime.datetime.today() - datetime.timedelta(days=value)


# class PlayLocalMusicTask(Task):
#     def __init__(self, hr, mn, path, n, type=3 ,pause_days = 0):
#         self.path = path
#         self.n = n
#         super(PlayLocalMusicTask, self).__init__(u"播放本地音乐",
#                                                  hr, mn, music.play_songs, (path, n, True), type,pause_days)
#
#     def __repr__(self):
#         return "%s(%s,%s,'%s',%s,%s,%s) " % (
#             self.__class__.__name__, self.t_hour, self.t_min, self.path, self.n, self.type, self.pause_days)
#


class PlayMusicTask(Task):
    def __init__(self, hr, mn,url, n, vol=None, type=3,pause_days = 0):
        self.url = url
        self.n = n
        self.vol = vol
        super(PlayMusicTask, self).__init__("music",
                                            hr, mn, music.play_songs, (url, n, True, vol), type, pause_days)

    def __repr__(self):
        return "%s(%s,%s,'%s',%s,%s,%s,%s) " % (
            self.__class__.__name__, self.t_hour, self.t_min, self.url, self.n, self.vol, self.type,self.pause_days)

class TellBusTask(Task):
    def __init__(self, hr, mn,bus_name,station,search_id, cnt=15, interval=60, type=1,pause_days = 0):
        self.bus_name = bus_name
        self.station = station
        self.search_id = search_id
        self.cnt = cnt
        self.interval = interval
        super(TellBusTask, self).__init__("bus",hr, mn, gz_bus.tell_bus, (bus_name,station,search_id,cnt,interval),type,pause_days)

    def __repr__(self):
        return "%s(%s,%s,'%s','%s','%s',%s,%s,%s,%s) " % (
            self.__class__.__name__, self.t_hour, self.t_min,self.bus_name,self.station,self.search_id, self.cnt, self.interval,self.type, self.pause_days)

class TellWeatherTask(Task):
    def __init__(self, hr, mn, d = True, t=False, type=3,pause_days = 0):
        self.d = d
        self.t = t
        super(TellWeatherTask, self).__init__("weather", hr, mn, weather.tell_today, (d,t),type,pause_days)

    def __repr__(self):
        return "%s(%s,%s,%s,%s,%s,%s) " % (
            self.__class__.__name__, self.t_hour, self.t_min, self.d, self.t, self.type, self.pause_days)


class ReadTextTask(Task):
    def __init__(self, hr, mn, text, per=0, type=3,pause_days = 0):
        self.text = text
        self.per = per
        super(ReadTextTask, self).__init__('read', hr, mn, baidu_tts.read_aloud, (text,False,5,5,9,per), type,pause_days)
    def __repr__(self):
        return "%s(%s,%s,'%s',%s,%s,%s) "%(self.__class__.__name__,self.t_hour,self.t_min,self.text,self.per,self.type,self.pause_days)




















@tell_time.tell_time_first
def load_weather(d=True,t=False):
    """
        d:穿衣建议
        t:出行建议
    """
    baidu_tts.read_aloud(weather.today(d, t), per=3)




from music.xm_music import xiami
from random import randint
def auto_check_in():
    sleep_secs = randint(0,1800)
    log.info(u'将在%d秒后进行虾米签到。'%sleep_secs)
    time.sleep(sleep_secs)
    x = xiami()
    ret = x.check_in()
    if ret:
        util.sendEmail('hyiit@qq.com','虾米签到失败',ret)



def load_all_tasks():
    tasks = {}
    names = config.config.options('Task')
    for name in names:
        tasks[name] = eval(config.config.get('Task',name))
    return tasks

def save_all_tasks(tasks):
    for name in tasks.keys():
        config.set('Task',name,tasks[name])
    config.save()


def save_task(name,task):
    config.set("Task",name,task)
    config.save()



tasks = load_all_tasks()










if __name__ == '__main__':
    #
    # rtt = ReadTextTask(8,10,"你是呆逼吗？")
    # print rtt

    # tasks = {
    #     'db': ReadTextTask(14,59,"你是呆逼吗？"),
    #     'xm': Task("虾米签到", 9, 0, auto_check_in),
    #     'weather1': TellWeatherTask(14, 56),
    #     'wy': PlayMusicTask(15, 58, "http://music.163.com/#/playlist?id=326005981", 5,pause_days=2)
    # }
    tasks = load_all_tasks()
    # save_all_tasks(tasks)
    # print task.tasks
    from threading import Timer
    import time

    for tktk in tasks:
        if isinstance(tasks[tktk],PlayMusicTask):
            print tasks[tktk]

    t = time.localtime()
    for name in tasks:
        tk = tasks[name]
        if t.tm_hour == tk.t_hour and tk.t_min >= t.tm_min:
            if tk.pause_days == 0:
                interval = (tk.t_min - t.tm_min) * 60 - t.tm_sec
                interval = max(0, interval)
                log.warn(u"将在%s秒后执行任务：%s - %s。" % (interval, name, tk.name))
                Timer(interval, tk.func, tk.args).start()
            elif tk.pause_days > 0:
                tk.pause_days -= 1
                save_task(name,tk)