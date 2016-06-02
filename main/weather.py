# coding=utf-8
city = 'guangzhou'
url = 'http://apis.baidu.com/heweather/weather/free?city=%s' % city
from common.secret_const import baidu_apistore_api_key as api_key
# 返回结果说明：http://apistore.baidu.com/apiworks/servicedetail/478.html
import logging
log = logging.getLogger(__name__)
import datetime

import baidu_tts
from common.util import getJson,byteify

header = {'apikey': api_key}






def today(drsg = True, trav = False):

    json = byteify(getJson(url, header=header))

    if 'HeWeather data service 3.0' not in json or json['HeWeather data service 3.0'][0]['status'] != 'ok':
        log.error("天气信息获取失败：%s" % json)
        return "天气信息获取失败"

    w = json['HeWeather data service 3.0'][0]
    now_tmp = w['now']['tmp']  # 当前温度

    today = datetime.date.today().strftime('%Y-%m-%d')



    fc = filter(lambda d:d['date']==today, w['daily_forecast'])
    if len(fc) == 1 :
        today_forecast = fc[0]
    else:
        log.error("无法获取今日天气：%s" % w['daily_forecast'])
        return "无法获取今日天气"
    d_cond = today_forecast['cond']['txt_d']  # 白天天气
    n_cond = today_forecast['cond']['txt_n']  # 夜间天气

    min_tmp = today_forecast['tmp']['min']
    max_tmp = today_forecast['tmp']['max']
    if w['suggestion']['comf']:
        comf = '舒适度：%s。' % w['suggestion']['comf']['brf']  # 舒适度
    else:
        comf = ''
    if drsg and w['suggestion']['drsg']:
        drsg = w['suggestion']['drsg']['txt']  # 穿衣建议
        drsg = drsg.replace('着','穿')       #播报时无法区分多音字
    else:
        drsg = ''
    if trav and w['suggestion']['trav']:
        trav = w['suggestion']['trav']['txt']  # 旅行建议
    else:
        trav = ''

    # # todo 根据降水概率提醒降水时间
    # rain = filter(lambda f: int(f['pop']) > 50, w['hourly_forecast'])
    # if rain:
    #     print(len(rain))
    #     for i in rain: print(i['date'],i['pop'])

    log.info("获取%s天气。更新日期：%s" % (today_forecast['date'], w['basic']['update']['loc']))
    return "现在气温%s度；今天白天：%s，夜间：%s，%s到%s度。%s%s%s" % \
           (now_tmp, d_cond, n_cond, min_tmp, max_tmp, comf, drsg, trav)


def day_of_week(days_after):
    """一周内的天气，days_after：几天后; 0即今天。"""

    if days_after == 0: return today()
    if days_after < 0 or days_after > 6: raise ValueError(u"日期需在[0-6]间")

    json = byteify(getJson(url, header=header))

    if 'HeWeather data service 3.0' not in json or json['HeWeather data service 3.0'][0]['status'] != 'ok':
        log.error("天气信息获取失败：%s" % json)
        return "天气信息获取失败"

    w = json['HeWeather data service 3.0'][0]

    day = datetime.date.today() +datetime.timedelta(days=days_after)
    day_str = day.strftime('%Y-%m-%d')

    fc = filter(lambda d: d['date'] == day_str, w['daily_forecast'])
    if len(fc) == 1:
        day_forecast = fc[0]
    else:
        log.error("无法获取%s的天气：%s" % (day.strftime('%m/%d'),w['daily_forecast']))
        return "无法获取%s的天气"%day.strftime('%m/%d')
    d_cond = day_forecast['cond']['txt_d']  # 白天天气
    n_cond = day_forecast['cond']['txt_n']  # 夜间天气

    min_tmp = day_forecast['tmp']['min']
    max_tmp = day_forecast['tmp']['max']


    log.info("获取%s天气。更新日期：%s" % (day_forecast['date'], w['basic']['update']['loc']))
    return "%s白天：%s，夜间：%s，%s到%s度。" % \
           (day.strftime('%m/%d'), d_cond, n_cond, min_tmp, max_tmp)



def tell_today(drsg = False, trav = False):
    w = today(drsg, trav)
    baidu_tts.read_aloud(w)

def tell_day_of_week(days_after=0):
    w = day_of_week(days_after)
    baidu_tts.read_aloud(w)

if __name__ == '__main__':
    print(today(trav=True))
    #baidu_tts.read_aloud(tell_today())

# 现在时间是上午7点50分，气温20度；今天白天：晴，夜间：晴，18到27度。舒适度：较舒适，建议着长袖T恤、衬衫加单裤等服装。年老体弱者宜着针织长袖衬衫、马甲和长裤。
# 晚上10点有较大概率会下雨。
