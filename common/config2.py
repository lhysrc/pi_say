# coding=utf-8

import ConfigParser,os
import logging
log = logging.getLogger(__name__)


CONFIG_PATH = './local/config.ini'

config = ConfigParser.ConfigParser()



def get_config(section,option):
    option = option.lower()
    if section not in config.sections():
        return None
    if option not in config.options(section):
        return None
    return config.get(section,option)

def set_config(section,option,value=""):
    """
        设置配置，请记得用save保存
    """
    if section not in config.sections():
        config.add_section(section)
    config.set(section,option,value)

def save():
    with open(CONFIG_PATH,'wb') as f:
        config.write(f)
    log.info("配置文件保存成功。")


all_configs = {
    "baidu_tts"     : ['apiKey','secretKey'],
    "email"         : ["address","password","smtpServer"],
    "weather"       : ["baidu_apistore_apiKey",'city'],
    "xiami"         : ["username","password"]
}
if not os.path.exists(CONFIG_PATH):
    log.info("配置文件不存在，将新建一个（%s），请填写相关信息。"%CONFIG_PATH)

    for k,vs in all_configs.items():        
        for v in vs:
            set_config(k,v)
    save()
else:
    with open(CONFIG_PATH,'rb') as f:
        config.readfp(f)

def get_weather_info():
    baidu_apistore_api_key = get_config("weather","baidu_apistore_apiKey")
    city = get_config("weather","city")
    return baidu_apistore_api_key,city

def get_xiami_info():
    return get_config("xiami","username"),get_config("xiami","password")

def get_baidu_tts_key():
    apiK = get_config("baidu_tts","apiKey")
    secretK = get_config("baidu_tts","secretKey")
    return apiK,secretK

def get_email_info():
    addr = get_config("email","address")
    pwd = get_config("email","password")
    smtp_svr = get_config("email","smtpServer")
    return addr,pwd,smtp_svr

if __name__ == '__main__':
    print get_baidu_tts_key()