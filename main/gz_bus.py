#coding=utf-8
import urllib

import baidu_tts

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
    import util
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

#res = ccxx_1_772()
#print res,len(res)
#print res[0]['count']