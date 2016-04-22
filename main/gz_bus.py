#coding=utf-8
import logging
import urllib

import baidu_tts
log = logging.getLogger(__name__)


url_main = 'http://wxbus.gzyyjt.net/'
urlGetStationByName = url_main + 'wei-bus-app/station/getByName'
urlGetRouteByName = url_main + 'wei-bus-app/route/getByName'
urlGetBusByStation = url_main + 'wei-bus-app/routeStation/getByStation/%s' # stationId
urlGetStationByRouteAndDirection = url_main+'wei-bus-app/routeStation/getByRouteAndDirection/%s/%s' # ri/d

urlWaitBusWaitTime = url_main + "wei-bus-app/waitBus/waitTime"

headers = {
    "Accept"         : "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Content-Type"   : "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer"        : "http://wxbus.gzyyjt.net/wei-bus-app/station",
    "User-Agent"     : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
    "Origin"         : "http://wxbus.gzyyjt.net",
    "DNT":1,

}

cookie = {
    'JSESSIONID' : '3FDFA7A164B15F33436BD56E73BBD6F7',
    'WBSRV' : 's3',
    'route' : 'fe9b13b33d88398957ee445b97555283',
}

import requests
ss = requests.session()
ss.headers.update(headers)


ss.cookies.update(cookie)

def search_station(name):
    """通过名称查找站点"""
    d = {'name':name}
    res = ss.post(urlGetStationByName, d)
    stations = res.json()
    #print stations
    # [{'i': '12344', 'n': '长兴路东站'},...]
    return stations

def search_route(name):
    """通过名称查找线路"""
    d = {'name':name}
    res = ss.post(urlGetRouteByName, d)
    routes = res.json()
    #print stations
    # [{'i': '713', 'n': 'B1路'},...]
    return routes

#print search_route('b1')

def get_all_route(stationid):
    """通过站点ID查找所有线路"""
    res = ss.get(urlGetBusByStation % stationid)
    buses = res.json()
    #print buses
    # [{"ri":"89","rn":"581路","rsi":"162545","d":"0","dn":"长福路(天河客运站)总站-黄埔客运站总站"},...]
    return buses['l'] if 'l' in buses else []

def get_all_station(route_id,direction_id):
    """通过线路ID和目的ID查找所有停靠站点"""
    res = ss.get(urlGetStationByRouteAndDirection % (route_id,direction_id))
    stations = res.json()
    # [{"i":"162566","n":"长福路(天河客运站)总站","sni":"5655","si":"7606"},...]
    return stations['l'] if 'l' in stations else []

def get_searchId(station_id,route_id,direction_id):
    stations = get_all_station(route_id,direction_id)
    station = filter(lambda s:s['sni']==station_id, stations)
    if station:return station[0]['i']


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
    result = util.getJson(urlWaitBusWaitTime, data)
    cnt, tm = result[0]['count'],result[0]['time']
    if read:
        if cnt == -1:
            baidu_tts.read_aloud(u"%s尚未发车" % bus_no, True,per=0)
        elif cnt == tm == 0:
            baidu_tts.read_aloud(u"%s已到达%s站" % (bus_no, st_name), True,per=0)
        else:
            baidu_tts.read_aloud(u"%s距%s还有%s站，预计在%s分钟后到达" %
                                 (bus_no, st_name, cnt, tm), True,per=0)
        if(cnt != -1 and len(result) > 1):
            cnt, tm = result[1]['count'], result[1]['time']
            if cnt==-1:
                baidu_tts.read_aloud(u"下一班尚未发车", True,per=0)
            else:
                baidu_tts.read_aloud(u"下一班还有%s站" % cnt, True,per=0)
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
    # return v

def pause_tell_bus(bus,days=1):
    v = config.get('bus', bus).split(';')
    v[0] = str(days)
    config.set('bus',bus,';'.join(v))
    config.save()

def get_pause_day(bus):
    v = config.get('bus', bus).split(';')
    return int(v[0])



status = {} # 报站状态
import config,time,threading
def tell_bus(bus_name,station,search_id,cnt = 15,interval = 60):
    status[search_id] = True
    for i in range(0,cnt):
        if not status[search_id]:break
        threading.Thread(target=count_waittime,args=(bus_name,station,search_id)).start()
        time.sleep(interval)
    status[search_id] = False


# from task2 import *
# t581 = Task('581',7,47,TELL_BUS,(581,"长兴路东",162545),holiday=False)
# t498 = Task('498',8,5,TELL_BUS,(498,"长兴路东",261508),holiday=False)
# tB11 = Task('B11',7,47,TELL_BUS,('b11', "长兴路东", 87792),holiday=False)
# tasks += [t581,t498,tB11]


if __name__ == '__main__':

    s = raw_input(u"1.通过站点查找\n2.通过班次查找\n")
    if s == '1':
        s = raw_input(u"请输入站点：\n")
        stations = search_station(s)
        for i, b in enumerate(stations): print i, b['n'], b['i']
        s = raw_input(u"第几个？")
        stationid = stations[int(s)]['i']
        print "stationid ",stationid
        #
        buses = get_all_route(stationid)
        for i,b in enumerate(buses):print i,b['rn'],b['dn']
        s = raw_input(u"第几条？")
        bus = buses[int(s)] #filter(lambda b:b['rsi']=='162545',buses)[0]


        #print bus['ri']

        ri,d = bus['ri'],bus['d']
        sid = get_searchId(stationid,ri,d)
        print "该站点查询ID为：",sid
    elif s == '2':
        s = raw_input(u"请输入班次：\n")
        routes = search_route(s)
        for i, r in enumerate(routes): print i, r['n'], r['i']
        s = raw_input(u"第几个？")
        rid = routes[int(s)]['i']
        s,d='-1',1
        while s=='-1':
            d=(d+1)%2
            stations = get_all_station(rid,d )
            for i, st in enumerate(stations): print i,st['n'],st['i']
            s = raw_input(u"第几个？查看返程输入-1")
        stationid = stations[int(s)]['i']
        print "stationid ", stationid

    else:
        pass

