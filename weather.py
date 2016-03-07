# coding=utf-8

city = 'guangzhou'
url = 'http://apis.baidu.com/heweather/weather/free?city=%s' % city
api_key = '6aaa80cda8ee541ad53047b6ce6b8468'
#返回结果说明：http://apistore.baidu.com/apiworks/servicedetail/478.html

import util
header = {'apikey':api_key}
json = util.getJson(url,header=header)

def byteify(input): #解决网络获取数据前带u的问题
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:return input

json = byteify(json)
if 'HeWeather data service 3.0' not in json or json['HeWeather data service 3.0'][0]['status']!='ok':
    print("天气信息获取失败，获取结果为：\n%s" % json )

w = json['HeWeather data service 3.0'][0]


now_tmp = w['now']['tmp']            #当前温度

today_forecast =  w['daily_forecast'][0]
d_cond = today_forecast['cond']['txt_d']    #白天天气
n_cond = today_forecast['cond']['txt_n']    #夜间天气

min_tmp = today_forecast['tmp']['min']
max_tmp = today_forecast['tmp']['max']

comf = w['suggestion']['comf']['brf'] #舒适度
drsg = w['suggestion']['drsg']['txt'] #穿衣建议



rain = filter(lambda f:int(f['pop'])>50,w['hourly_forecast'])
if rain:
    print(len(rain))
    for i in rain:print(i['date'])

print "%s。" % max_tmp
print "现在气温%s；今天白天：%s，夜间：%s，%s到%s度。舒适度：%s，%s。" % (now_tmp,d_cond,n_cond,min_tmp,max_tmp,comf,drsg)


#现在时间是上午7点50分，气温20度；今天白天：晴，夜间：晴，18到27度。舒适度：较舒适，建议着长袖T恤、衬衫加单裤等服装。年老体弱者宜着针织长袖衬衫、马甲和长裤。
#晚上10点有较大概率会下雨。