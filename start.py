# coding=utf-8
import os,time,gz_bus,baidu_tts
if(not os.path.exists("./tmp")): os.mkdir("./tmp")
if(not os.path.exists("./music")): os.mkdir("./music")

def tell_time():
    t = time.localtime()
    baidu_tts.read_aloud("现在时间是%s点%s分" % (t.tm_hour,t.tm_min))
    first_sleep = 3600 - time.localtime().tm_min*60 - time.localtime().tm_sec
    print("现在时间：%s点%s分，距离下次报时还有%s秒" % (t.tm_hour,t.tm_min,first_sleep))
    time.sleep(first_sleep)
    while True:
        t = time.localtime()
        str = "现在时间是%s点整" % (t.tm_hour) \
            if t.tm_min == 0 else "现在时间是%s点%s分" % (t.tm_hour,t.tm_min)
        baidu_tts.read_aloud(str)
        time.sleep(3600 - time.localtime().tm_min*60 - time.localtime().tm_sec)


def _498():
    while True:
        print("498")
        gz_bus.cxld_0_498()
        time.sleep(60)

def _581():
    while True:
        print("581")
        gz_bus.cxld_0_581()
        time.sleep(60)



if __name__ == '__main__':
    import threading
    t = threading.Thread(target=tell_time)
    t.start()
    # t1 = threading.Thread(target=_498)
    # t2 = threading.Thread(target=_581)
    # print("start _498")
    # t1.start()
    # print("wait 30'")
    # time.sleep(30)
    # print("start _581")
    # t2.start()

