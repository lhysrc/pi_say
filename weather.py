# coding=utf-8

city = 'guangzhou'
url = 'http://apis.baidu.com/heweather/weather/free?city=%s' % city
api_key = '6aaa80cda8ee541ad53047b6ce6b8468'
#返回结果说明：http://apistore.baidu.com/apiworks/servicedetail/478.html

import util
header = {'apikey':api_key}
json = util.getJson(url,header=header)

if 'HeWeather data service 3.0' not in json:
    print("天气信息获取失败，获取结果为：\n%s" % json )

w = json['HeWeather data service 3.0'][0]


now_tmp = w['now']['tmp']            #当前温度
drsg =w['suggestion']['drsg']['txt'] #穿衣建议
today_forecast =  w['daily_forecast'][0]


print "%s,%s" % (now_tmp, drsg)