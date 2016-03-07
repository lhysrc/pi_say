# coding=utf-8

city = 'guangzhou'
url = 'http://apis.baidu.com/heweather/weather/free?city=%s' % city
api_key = '6aaa80cda8ee541ad53047b6ce6b8468'
# 返回结果说明：http://apistore.baidu.com/apiworks/servicedetail/478.html

from util import getJson,byteify

header = {'apikey': api_key}






def tell_today():

    json = byteify(getJson(url, header=header))

    if 'HeWeather data service 3.0' not in json or json['HeWeather data service 3.0'][0]['status'] != 'ok':
        print(json)
        return "天气信息获取失败"

    w = json['HeWeather data service 3.0'][0]

    now_tmp = w['now']['tmp']  # 当前温度

    today_forecast = w['daily_forecast'][0]
    d_cond = today_forecast['cond']['txt_d']  # 白天天气
    n_cond = today_forecast['cond']['txt_n']  # 夜间天气

    min_tmp = today_forecast['tmp']['min']
    max_tmp = today_forecast['tmp']['max']

    comf = w['suggestion']['comf']['brf']  # 舒适度
    drsg = w['suggestion']['drsg']['txt']  # 穿衣建议



    print "获取%s天气。" % today_forecast['date']
    return "现在气温%s度；今天白天：%s，夜间：%s，%s到%s度。舒适度：%s，%s" % \
           (now_tmp, d_cond, n_cond, min_tmp, max_tmp, comf, drsg)

    # # todo 根据降水概率提醒降水时间
    # rain = filter(lambda f: int(f['pop']) > 50, w['hourly_forecast'])
    # if rain:
    #     print(len(rain))
    #     for i in rain: print(i['date'])

if __name__ == '__main__':
    print(tell_today())
    import baidu_tts
    baidu_tts.read_aloud(tell_today())

# 现在时间是上午7点50分，气温20度；今天白天：晴，夜间：晴，18到27度。舒适度：较舒适，建议着长袖T恤、衬衫加单裤等服装。年老体弱者宜着针织长袖衬衫、马甲和长裤。
# 晚上10点有较大概率会下雨。
