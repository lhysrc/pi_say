# coding=utf-8

# 整点报时的起始小时和结束时间
FirstHour = 8
LastHour = 23

tell_range = range(FirstHour,LastHour + 1)


def hour_str(hour):
    if hour == 0:
        return "半夜12"
    elif hour == 12:
        return "中午12"
    elif hour in range(1, 6):
        return "凌晨%d" % hour
    elif hour in range(6, 12):
        return "上午%d" % hour
    elif hour in range(13, 18):
        return "下午%d" % (hour % 12)
    elif hour in range(18, 24):
        return "晚上%d" % (hour % 12)
    else:
        return "%d" % hour


import time

import baidu_tts
import logging
log = logging.getLogger(__name__)

def tell_time(t = None):
    if not t:
        t = time.localtime()
    s = get_strtime(t)
    baidu_tts.read_aloud_async(s, cache=t.tm_min == 0,per=0 if t.tm_min == 0 else 3)  # 缓存整点报时语音
    return t
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

def get_strtime(t = None):
    if not t:
        t = time.localtime()
    s = "现在时间是：%s点整" % hour_str(t.tm_hour) \
        if t.tm_min == 0 else "现在时间是：%s点%s分" % (hour_str(t.tm_hour), t.tm_min)
    return s

import functools
def tell_time_first(func):
    """
        加上此装饰器则会先报时再执行该函数
    """
    @functools.wraps(func)
    def wrapper(*args,**kw):
        tell_time()
        return func(*args,**kw)
    return wrapper

def print_time():
    print time.strftime('%Y-%m-%d %H:%M:%S')


def to_tuples(days):
    ret = []
    if not days:return ret
    for k,vs in days.items():
        for v in vs:
            ret.append((int(k),int(v)))
    return ret


import setting
Holiday = to_tuples(setting.get_setting('holiday'))
WorkdayInWeekend = to_tuples(setting.get_setting('workday_in_weekend'))

def is_workday(time):
    m,d = time.tm_mon,time.tm_mday
    if (m,d) in Holiday:return False
    if (m,d) in WorkdayInWeekend:return True

    return time.tm_wday < 5

def tell_time_repeat(interval, cnt):
    """
    报时
    Args:
        interval: 间隔，每interval分钟报时一次
        cnt: 次数
    Returns:None
    """
    while cnt:
        t = time.localtime()
        if t.tm_min != 0 or (t.tm_hour not in tell_range): # 整点已报时，帮若在整点报时的时间段里，0分不需要再报时。
            tell_time(t)
        cnt -= 1
        time.sleep(interval*60)









if __name__ == '__main__':
     t = time.localtime(time.mktime((2016,6,12,0,0,0,0,0,-1)))
     print(t,is_workday(t))