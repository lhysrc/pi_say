# coding=utf-8
from config import *
city = 'guangzhou'
url = 'http://apis.baidu.com/heweather/weather/free?city=%s' % city
api_key = BaiDu_API_STORE_API_KEY
# 返回结果说明：http://apistore.baidu.com/apiworks/servicedetail/478.html

from util import getJson,byteify
import log
import time

header = {'apikey': api_key}






def tell_today():

    json = byteify(getJson(url, header=header))

    if 'HeWeather data service 3.0' not in json or json['HeWeather data service 3.0'][0]['status'] != 'ok':
        log.WARN("天气信息获取失败：%s" % json)
        return "天气信息获取失败"

    w = json['HeWeather data service 3.0'][0]
    now_tmp = w['now']['tmp']  # 当前温度

    today = time.strftime('%Y-%m-%d')

    fc = filter(lambda d:d['date']==today, w['daily_forecast'])
    if len(fc) == 1 :
        today_forecast = fc[0]
    else:
        log.WARN("无法获取今日天气：%s" % w['daily_forecast'])
        return "无法获取今日天气"
    d_cond = today_forecast['cond']['txt_d']  # 白天天气
    n_cond = today_forecast['cond']['txt_n']  # 夜间天气

    min_tmp = today_forecast['tmp']['min']
    max_tmp = today_forecast['tmp']['max']

    comf = w['suggestion']['comf']['brf']  # 舒适度
    drsg = w['suggestion']['drsg']['txt']  # 穿衣建议

    # # todo 根据降水概率提醒降水时间
    # rain = filter(lambda f: int(f['pop']) > 50, w['hourly_forecast'])
    # if rain:
    #     print(len(rain))
    #     for i in rain: print(i['date'],i['pop'])

    log.INFO("获取%s天气。更新日期：%s" % (today_forecast['date'], w['basic']['update']['loc']))
    return "现在气温%s度；今天白天：%s，夜间：%s，%s到%s度。舒适度：%s，%s" % \
           (now_tmp, d_cond, n_cond, min_tmp, max_tmp, comf, drsg)


if __name__ == '__main__':
    print(tell_today())
    import baidu_tts
    #baidu_tts.read_aloud(tell_today())

# 现在时间是上午7点50分，气温20度；今天白天：晴，夜间：晴，18到27度。舒适度：较舒适，建议着长袖T恤、衬衫加单裤等服装。年老体弱者宜着针织长袖衬衫、马甲和长裤。
# 晚上10点有较大概率会下雨。
