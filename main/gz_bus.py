#coding=utf-8
import logging
import urllib

import baidu_tts
log = logging.getLogger(__name__)
wait_time_url = "http://wxbus.gzyyjt.net/wei-bus-app/waitBus/waitTime"

def count_waittime(bus_no,st_name,search_num,num=2,read=True):
    """根据公车号，站点名，查询编码查找到站信息
    Args:
        bus_no:公交车号
        st_name:站点名
        search_num:网站上的查询码
        num:查询要返回的条数
        read:是否朗读
    Returns:
        [{"count":2,"time":5},{"count":-1,"time":-1}]
        count:距离站点
        time:预计等待时间
    """
    param = {"rsId":search_num,"num":num}
    data = urllib.urlencode(param)
    from common import util
    result = util.getJson(wait_time_url, data)
    cnt, tm = result[0]['count'],result[0]['time']
    if read:
        if cnt == -1:
            baidu_tts.read_aloud("%s尚未发车" % bus_no, True,per=0)
        elif cnt == tm == 0:
            baidu_tts.read_aloud("%s已到达%s站" % (bus_no, st_name), True,per=0)
        else:
            baidu_tts.read_aloud("%s距%s还有%s站，预计在%s分钟后到达" %
                                 (bus_no, st_name, cnt, tm), True,per=0)
        if(cnt != -1 and len(result) > 1):
            cnt, tm = result[1]['count'], result[1]['time']
            if cnt==-1:
                baidu_tts.read_aloud("下一班尚未发车", True,per=0)
            else:
                baidu_tts.read_aloud("下一班还有%s站" % cnt, True,per=0)
    return result

def ccxx_1_772():
    """772往天河客运站，岑村小学到站信息"""
    return count_waittime(772,"岑村小学",156257)

def cxld_0_498():
    """498往天河客运站，长兴路东到站信息"""
    return count_waittime(498,"长兴路东",261508)

def cxld_0_581():
    """581往科学城，长兴路东到站信息"""
    return count_waittime(581,"长兴路东",162545)

def cxld_0_b11():
    """b11往员村方向，长兴路东到站信息 87792 ,返程87995"""
    return count_waittime('b11', "长兴路东", 87792)

#res = ccxx_1_772()
#print res,len(res)
#print res[0]['count']


#       配置说明
#    581 = 0;7,48;60;15
#  公交车 = 暂停天数（不含假日）;开始报站时间;间隔秒;次数
import config,time,threading
def baozhan(bus,func):
    v = config.get('bus',bus).split(';')
    pause_days,interval,cnt = int(v[0]),int(v[2]),int(v[3])
    if pause_days<0:
        #print "%s不报站"%bus
        log.warn("%s不报站"%bus)
    elif pause_days>0:
        log.warn("今日%s暂停报站，将在%d天后恢复报站。"%(bus,pause_days))
        config.set('bus',bus,'%d;%s;%d;%d'%(pause_days-1,v[1],interval,cnt))
        config.save()
    else:
        for i in range(0,cnt):
            threading.Thread(target=func).start()
            time.sleep(interval)
    return v


def pause_tell_bus(bus,days=1):
    v = config.get('bus', bus).split(';')
    v[0] = str(days)
    config.set('bus',bus,';'.join(v))
    config.save()

def get_pause_day(bus):
    v = config.get('bus', bus).split(';')
    return int(v[0])