# coding=utf-8

# 节日	时间	调休上班	天数
# 元旦	1/1-1/3	与周末连休	3天
# 春节	2/7-2/13	2月6日、14日上班	7天
# 清明节	4/2-4/4	与周末连休	3天
# 劳动节	4/30-5/2	5月2日补休	3天
# 端午节	6/9-6/11	6月12日上班	3天
# 中秋节	9/15-9/17	9月18日上班	3天
# 国庆节	10/1-10/7	10月8日、9日上班	7天

import ConfigParser,os
import logging
log = logging.getLogger(__name__)
CONFIG_PATH = './local/cfg.ini'
if not os.path.exists(CONFIG_PATH):
    open(CONFIG_PATH,'w+').close()

config = ConfigParser.ConfigParser()
if 'baidu_tts' not in config.sections(): config.add_section("baidu_tts")
with open(CONFIG_PATH,'rb') as f:
     config.readfp(f)
# print(config.get('baidu_tts','token'))




def get(section,option):
    if section not in config.sections():
        return None
    if option not in config.options(section):
        return None
    return config.get(section,option)

def set(section,option,value=None):
    """
        设置配置，请记得用save保存
    """
    if section not in config.sections():
        config.add_section(section)
    config.set(section,option,value)
    #save_config()


def save():
    with open(CONFIG_PATH,'wb') as f:
        config.write(f)
    log.info("配置文件保存成功。")

def get_baidu_tts_token():
    return get('baidu_tts','token')

def set_baidu_tts_token(token):
    set('baidu_tts','token',token)
    save()


def get_days(sec_name):
    opts = config.options(sec_name)
    ret = []
    for m in opts:
        v = get(sec_name,m)
        ds = [int(s) for s in v.split(';')]
        ret+=[(int(m),d) for d in ds]
    return ret

if __name__ == '__main__':
    # import json
    # json.dump(Holiday_2016,open('json.json','wb'))



    # print([tuple(a) for a in json.load(open('json.json','rb'))])
    # print(config.options('baidu_tts'))
    # print((get('day','holiday')))
    # print( [6,12] in get('day','holiday'))

    Holiday_2016 = [
                       (4, 2), (4, 3), (4, 4),
                       (4, 30), (5, 1), (5, 2),
                       (6, 9), (6, 10), (6, 11),
                       (9, 15), (9, 16), (9, 17),
                   ] + [(10, i) for i in range(1, 8)]
    WorkdayInWeekend_2016 = [
        (6, 12), (9, 18), (10, 8), (10, 9)
    ]
    def save_days(days_tuple_list,sec_name):

        for (m,d) in days_tuple_list:
            (m,d) = (str(m),str(d))
            vs = get(sec_name,m)
            if vs:
                vs = vs.split(';')
                if d not in vs: vs.append(d)
                set(sec_name,m,';'.join(vs))
            else:
                set(sec_name,m,'%s'%d)
        save()



    print(get_days('holiday'))
    print(get_days('workday_in_weekend'))
    # save_days(Holiday_2016,'holiday')
    # save_days(WorkdayInWeekend_2016,'workday_in_weekend')

    #print config.has_option('baidu_tts','token')