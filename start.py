#! /usr/bin/py
# coding=utf-8
import os, time, gz_bus, baidu_tts ,weather
from tell_time import *
if not os.path.exists("./tmp"): os.mkdir("./tmp")
if not os.path.exists("./music"): os.mkdir("./music")



# class mytimer:
#     def __init__(self,func,start_time=(0,0)):
#         """
#         Args:
#             start_time (tuple): 启动任务的时间
#         """
#         self.start_time = start_time
#         self.func = func


def bao_zhan():
    i = 40
    while i:
        if i < 25:
            print("498")
            gz_bus.cxld_0_498()
        if i > 15:
            print("581")
            gz_bus.cxld_0_581()

        i -= 1
        time.sleep(60)

import play_sound
@tell_time_first
def alarm_song():
    play_sound.play("music/music.mp3")


@tell_time_first
def test():
    print('test tell time')

@tell_time_first
def load_weather():
    baidu_tts.read_aloud(weather.tell_today())

task_list = {
    (7, 45): (bao_zhan, ()),
    (7, 40): (alarm_song, ()),
    #(22, 11): (alarm_song, ())
    (7, 50): (load_weather, ())
}

if __name__ == '__main__':
    import threading, sched

    # bao_shi = threading.Thread(target=tell_time)
    # bao_shi.start()
    baidu_tts.read_aloud("程序开始运行",True)
    while True:
        t = time.localtime()
        if t.tm_wday in range(5) and t.tm_hour in [7, 8, 20, 21, 22, 23, 0]:
            tell_time(t)
        if t.tm_wday in [5,6] and t.tm_hour in [0] + range(8,24):
            tell_time(t)
        # if t.tm_hour == 7:
        #     threading.Timer(45 * 60, bao_zhan, ()).start()  # 7:45 报站
        #     threading.Timer(40 * 60, alarm_song, ()).start()  # 7:40 放歌
        print_time()
        for task_time,task_func in task_list.items():
            if t.tm_hour == task_time[0] and task_time[1] >= t.tm_min:
                interval = (task_time[1] - t.tm_min) * 60
                print("将在%s秒后执行%s" % (interval, task_func[0].__name__))
                threading.Timer(interval, task_func[0], task_func[1]).start()  # 7:45 报站

        # if t.tm_hour == 21:
        #     threading.Timer(10,alarm_song,()).start()
        #     threading.Timer(5,bao_zhan,()).start()
        time.sleep(3600 - time.localtime().tm_min * 60 - time.localtime().tm_sec)

        # t1 = threading.Thread(target=_498)
        # t2 = threading.Thread(target=_581)
        # print("start _498")
        # t1.start()
        # print("wait 30'")
        # time.sleep(30)
        # print("start _581")
        # t2.start()
