#! /usr/bin/py
# coding=utf-8

import os
import threading
required_dirs = ['tmp','music','log']
for d in required_dirs:
    if not os.path.exists(d): os.mkdir(d)

from main.tell_time import *
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


from main import ne_music, log, gz_bus, weather, play_sound


@tell_time_first
def alarm_song():
    try:
        ne_music.play_a_random_song()
    except Exception as e:
        log.ERROR(e)
        play_sound.play("music/music.mp3")


@tell_time_first
def load_weather():
    baidu_tts.read_aloud(weather.tell_today(), per=3)


def play_song_list():
    ne_music.play_a_list(n=10)

def start_main():



    workday_task_list = {
        (7, 50): (bao_zhan, ()),
        (7, 40): (alarm_song, ()),
        #(23, 01): (alarm_song, ()),
        (7, 45): (load_weather, ()),
        # (21, 10): (play_song_list, ()),
    }

    holiday_task_list ={
        (8, 45): (load_weather, ()),
        (9, 00): (play_song_list, ()),
        (9, 50): (load_weather, ()),
    }

    # bao_shi = threading.Thread(target=tell_time)
    # bao_shi.start()
    log.INFO("程序开始运行")
    baidu_tts.read_aloud("程序开始运行", True)
    while True:
        t = time.localtime()
        wd = is_workday(t)
        # if t.tm_hour in range(1,7) : pass   #凌晨1到6点不报时
        time_range = [7, 8] + range(19, 24) if wd else [0] + range(8, 24)
        if t.tm_hour in time_range:
            tell_time(t)

        task_list = workday_task_list if wd else holiday_task_list
        for task_time,task_func in task_list.items():
            if t.tm_hour == task_time[0] and task_time[1] > t.tm_min:
                interval = (task_time[1] - t.tm_min) * 60 - t.tm_sec
                log.INFO("将在%s秒后执行%s" % (interval, task_func[0].__name__))
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


# import www
# if __name__ == '__main__':
#     import threading
#     #td = threading.Thread(target=main)
#     #td.start()
#     from www import run_app
#     run_app()
if __name__ == '__main__':
    threading.Timer(0, alarm_song, ()).start()
    start_main()
    #threading.Thread(target=start_main).start()
    #alarm_song()
    #www.run_app()
