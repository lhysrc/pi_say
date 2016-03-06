#! /usr/bin/py
# coding=utf-8
import os, time, gz_bus, baidu_tts

if not os.path.exists("./tmp"): os.mkdir("./tmp")
if not os.path.exists("./music"): os.mkdir("./music")

def hour_str(hour):
        if hour == 0 : return "半夜12"
        elif hour == 12 : return "中午12"
        elif hour in range(1,6) : return "凌晨%d" % hour
        elif hour in range(6,12) : return "上午%d" % hour
        elif hour in range(13,18) : return "下午%d" % (hour % 12)
        elif hour in range(18,24) : return "晚上%d" % (hour % 12)
        else : return "%d" % hour


# class mytimer:
#     def __init__(self,func,start_time=(0,0)):
#         """
#         Args:
#             start_time (tuple): 启动任务的时间
#         """
#         self.start_time = start_time
#         self.func = func


def tell_time():
    t = time.localtime()
    baidu_tts.read_aloud("现在时间是：%s点%s分" % (hour_str(t.tm_hour), t.tm_min))
    # first_sleep = 3600 - time.localtime().tm_min * 60 - time.localtime().tm_sec
    # print("现在时间：%s点%s分，距离下次报时还有%s秒" % (hour_str(t.tm_hour), t.tm_min, first_sleep))
    # time.sleep(first_sleep)
    # while True:
    #     t = time.localtime()
    #     if t.tm_hour in [7, 8, 20, 21, 22, 23, 0]:
    #         s = "现在时间是：%s点整" % hour_str(t.tm_hour) \
    #             if t.tm_min == 0 else "现在时间是：%s点%s分" % (hour_str(t.tm_hour), t.tm_min)
    #         baidu_tts.read_aloud(s)
    #     print("现在时间：%s点%s分，距离下次报时还有%s秒" % (hour_str(t.tm_hour), t.tm_min, first_sleep))
    #     time.sleep(3600 - time.localtime().tm_min * 60 - time.localtime().tm_sec)


def bao_zhan():
    i = 40
    while i:
        if i<30:
            print("498")
            gz_bus.cxld_0_498()
        if i>15:
            print("581")
            gz_bus.cxld_0_581()

        i -= 1
        time.sleep(60)

def alarm_song():
    import play_sound
    play_sound.play(u"music/不痛.mp3")

if __name__ == '__main__':
    import threading,sched

    # bao_shi = threading.Thread(target=tell_time)
    # bao_shi.start()


    while True:
        t = time.localtime()
        if t.tm_hour in [7, 8, 20, 21, 22, 23, 0]:
            s = "现在时间是：%s点整" % hour_str(t.tm_hour) \
                if t.tm_min == 0 else "现在时间是：%s点%s分" % (hour_str(t.tm_hour), t.tm_min)
            baidu_tts.read_aloud(s)
        if t.tm_hour == 7:
            threading.Timer(45*60,bao_zhan,()).start()      # 7:45 报站
            threading.Timer(40*60,alarm_song,()).start()    # 7:40 放歌
        # if t.tm_hour == 21:
        #     threading.Timer(10,alarm_song,()).start()
        #     threading.Timer(5,bao_zhan,()).start()

        # time.sleep(5)
        time.sleep(3600 - time.localtime().tm_min * 60 - time.localtime().tm_sec)

    # t1 = threading.Thread(target=_498)
    # t2 = threading.Thread(target=_581)
    # print("start _498")
    # t1.start()
    # print("wait 30'")
    # time.sleep(30)
    # print("start _581")
    # t2.start()
