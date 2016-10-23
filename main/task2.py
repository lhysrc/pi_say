# coding=utf-8
import uuid

# import config
import setting
import itertools,json
import music
from threading import Timer
import time
from logging import getLogger

from common import util

log = getLogger(__name__)
from main import tell_time
from main.gz_bus import tell_bus
from main.weather import tell_today,today
from main.baidu_tts import read_aloud_async

TASK_SAVE_PATH = './local/task.json'

MUSIC,TELL_BUS,TELL_WEATHER,READ_TEXT,TELL_TIME = 'music','bus','weather','read','time'
task_types = {
    MUSIC       : music.play_songs,
    TELL_BUS    : tell_bus,
    TELL_WEATHER: tell_today,
    READ_TEXT   : read_aloud_async,
    TELL_TIME   : tell_time.tell_time_repeat,
}

class Task(object):
    def __init__(self, hour, min, type,args=(), workday=False,holiday=False, pause_days=0, id=None):
        self.type = type # 类型或函数
        self.args = tuple(args)
        self.hour = hour
        self.min = min
        self.workday = workday
        self.holiday = holiday
        self.pause_days = pause_days
        self.id = str(uuid.uuid4()) if not id else id

    def __repr__(self):
         return str(self.__dict__) if self.type in task_types else '<PreTask_%s>' % self.type

    def to_dict(self,include_id = False):
        if self.type not in task_types:return None
        d = self.__dict__.copy()
        if not include_id:
            del d['id']
        return d


def load_all_tasks():
    tks = setting.load(TASK_SAVE_PATH)
    log.info("已加载%d条任务。"%len(tks))
    for t in tks:
        tasks.append(Task(**t))
    # for tp in task_types:
    #     d = config.get('Task',tp)
    #     if d:
    #         j = json.loads(d,encoding='utf-8')
    #         for t in j:
    #             tasks.append(Task(**t))


# def save_all_tasks():
#     for k,g in itertools.groupby(tasks,key=lambda t:t.type):
#         if k in task_types:
#             g = map(lambda t:t.to_dict(),g)
#             config.set('Task', k, json.dumps(g,encoding='utf-8'))
#     config.save()

def save_all_tasks():
    # for tp in task_types:
    #     tks = filter(lambda t:t.type == tp,tasks)
    #     tks = map(lambda t: t.to_dict(), tks)
    #     config.set('Task', tp, json.dumps(tks,encoding='utf-8'))
    # config.save()
    tks = map(lambda t: t.to_dict(), tasks)
    tks = filter(lambda t:t is not None,tks)
    setting.save(TASK_SAVE_PATH,tks)
    log.info("已保存所有任务。")

# def save_task(task):
#     if task.task_type_or_func not in task_types: return # todo 分任务类型存？任务不多没必要
#     name = task.task_type_or_func
#     task_to_save
#     config.set("Task",name,task)
#     config.save()
@tell_time.tell_time_first
def alarm_song():
    try:
        music.player.playing_volume = 30
        music.play_songs('http://music.163.com/#/discover/toplist?id=3778678',vol=30)
    except:
        log.exception("播放闹钟音乐出错。")
        music.player.stop()
        music.play_songs(vol=30)

@tell_time.tell_time_first
def tell_weather(d=True,t=False):
    """
        d:穿衣建议
        t:出行建议
    """
    read_aloud_async(today(d, t), per=3)

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

#
# def tell_time_every_10min(times=6):
#     while times:
#         t = time.localtime()
#         if t.tm_min != 0:
#             tell_time.tell_time(t)
#         times -= 1
#         time.sleep(60*10)

tasks = [ # Task(7, 35, alarm_song, (),workday=True),
          # Task(7, 43, tell_weather, (),workday=True),
          # Task(7, 50, tell_time_every_10min, (),workday=True),
          #
          # Task(8, 45, tell_weather, (),holiday=True),
          # Task(9, 45, tell_weather, (False,True),holiday=True),

          Task(9,  0, auto_check_in, (), workday=True, holiday=True),
          ]

if __name__ == '__main__':
    tasks += [Task(7, 47, TELL_BUS, (581, "长兴路东", 162545), workday=True),
              Task(7, 47, TELL_BUS, ('b11', "长兴路东", 87792), workday=True),
              Task(8,  5, TELL_BUS, (498, "长兴路东", 261508), workday=True),

              Task(7, 35, MUSIC, ('http://music.163.com/#/discover/toplist?id=3778678',1,True,30), workday=True),
              Task(10, 00, MUSIC, ('http://music.163.com/#/discover/toplist?id=3778678',10,True,50), holiday=True),
              Task(22, 45, MUSIC, ('./music_files/4baby',5,True,80), workday=True, holiday=True),

              # Task(21, 30, TELL_WEATHER, (0,), workday=True),
              Task(8, 5, READ_TEXT, ('呆逼呆逼起床了！',False,5,5,9,3,5), workday=True, holiday=False),
              ]

    save_all_tasks()
    # read_aloud_async('呆逼呆逼起床了！', per=0)
    # tasks += [Task(7, 47, TELL_BUS, (581, "长兴路东", 162545), workday=True),
    #           Task(8, 5, TELL_BUS, (498, "长兴路东", 261508), workday=True),
    #           Task(7, 47, TELL_BUS, ('b11', "长兴路东", 87792), workday=True),
    #           Task(7, 35, MUSIC, (), workday=True),
    #           Task(21, 30, TELL_WEATHER, (0,), workday=True),
    #           Task(21, 16, READ_TEXT, ('你是呆逼吗',), workday=True, holiday=False),
    #           Task(9,0,max,())
    # ]

    # save_all_tasks()


def start_tasks():
    log.info(u"程序开始运行")
    read_aloud_async("程序开始运行", True, per=0)

    load_all_tasks()    

    while True:
        t = time.localtime()
        wd = tell_time.is_workday(t)        
        time_range = tell_time.tell_range # [7, 8] + list(range(19, 24)) if wd else [0] + list(range(8, 24))
        if t.tm_hour in time_range:
            tell_time.tell_time(t)

        f_tks = filter(lambda tk:tk.workday if wd else tk.holiday,tasks)


        task_changed = False
        for task in f_tks:
            if t.tm_hour == task.hour and task.min >= t.tm_min:
                func = task_types[task.type] \
                    if task.type in task_types else task.type
                if task.pause_days == 0:
                    interval = (task.min - t.tm_min) * 60 - t.tm_sec
                    interval = max(0, interval)
                    log.info(u"将在%s秒后执行任务：%s。|%s。" % (interval, func.__name__,task))
                    Timer(interval, func, task.args).start()
                elif task.pause_days > 0:
                    task.pause_days -= 1
                    task_changed = True
                    log.warn(u"今日不执行任务‘%s’，将于%s日后执行。|%s。" % (func.__name__, task.pause_days,task))
                else:
                    log.warn(u"任务‘%s’已停止。|%s。" % (func.__name__,  task))
        if task_changed: save_all_tasks()

        t = time.localtime()
        time.sleep(3600 - t.tm_min * 60 - t.tm_sec)