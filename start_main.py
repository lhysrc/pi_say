#! /usr/bin/py
# coding=utf-8

import os
import threading
import time
required_dirs = ['tmp','music','log']
for d in required_dirs:
    if not os.path.exists(d): os.mkdir(d)

from main import baidu_tts,tell_time
from main import ne_music, gz_bus, weather, play_sound
from main.log import log

def bao_zhan():
    i = 30
    while i:
        if i < 22:
            gz_bus.cxld_0_498()
        if i > 18:
            gz_bus.cxld_0_581()

        i -= 1
        time.sleep(60)






@tell_time.tell_time_first
def alarm_song():
    try:
        ne_music.play_a_list(n=1)
    except:
        log.exception("播放闹钟音乐出错。")
        play_sound.play_local_music(1)

@tell_time.tell_time_first
def load_weather():
    baidu_tts.read_aloud(weather.tell_today(), per=3)


def play_song_list():
    ne_music.play_a_list(n=10)

def start_main():



    workday_task_list = {
        (7, 47): (bao_zhan, ()),
        (7, 35): (alarm_song, ()),
        # (9, 39): (alarm_song, ()),
        (7, 43): (load_weather, ()),
        # (21, 10): (play_song_list, ()),
    }

    holiday_task_list ={
        (8, 45): (load_weather, ()),
        (9, 00): (play_song_list, ()),
        (9, 50): (load_weather, ('',True)),
        # (10, 18): (play_song_list, ()),
    }

    # bao_shi = threading.Thread(target=tell_time)
    # bao_shi.start()
    log.info("程序开始运行")
    baidu_tts.read_aloud("程序开始运行", True)
    while True:
        t = time.localtime()
        wd = tell_time.is_workday(t)
        # if t.tm_hour in range(1,7) : pass   #凌晨1到6点不报时
        time_range = [7, 8] + range(19, 24) if wd else [0] + range(8, 24)
        if t.tm_hour in time_range:
            tell_time.tell_time(t)

        task_list = workday_task_list if wd else holiday_task_list
        for task_time,task_func in task_list.items():
            if t.tm_hour == task_time[0] and task_time[1] >= t.tm_min:
                interval = (task_time[1] - t.tm_min) * 60 - t.tm_sec
                interval = max(0, interval)
                log.info("将在%s秒后执行%s" % (interval, task_func[0].__name__))
                threading.Timer(interval, task_func[0], task_func[1]).start()
        time.sleep(3600 - time.localtime().tm_min * 60 - time.localtime().tm_sec)

        # t1 = threading.Thread(target=_498)
        # t2 = threading.Thread(target=_581)
        # print("start _498")
        # t1.start()
        # print("wait 30'")
        # time.sleep(30)
        # print("start _581")
        # t2.start()


from www import app
if __name__ == '__main__':
    log.info('-'*50)

    td = threading.Thread(target=start_main)
    if not app.debug: td.start()

    app.run(port=3080,threaded=True)
# if __name__ == '__main__':
#     #threading.Timer(0, alarm_song, ()).start()
#     start_main()
#     #threading.Thread(target=start_main).start()
#     #alarm_song()
#     #www.run_app()
