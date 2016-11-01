# coding=utf-8
import json,os,logging
SETTING_PATH = "./local/setting.json"

log = logging.getLogger(__name__)

setting = {}
"""
    "baidu_tts_token":"这是token",
    "holiday":{
        10:[1,2,3,4,5,6,7]
    },
    "workday_in_weekend":{

    }
}
"""

def load(path):
    with open(path,"r+") as f:
        return json.load(f,encoding='utf-8')

def save(path,setting):
    with open(path,"w+") as f:
        json.dump(setting,f,encoding='utf-8')

def set_setting(key,value):
    setting[key] = value
    save(SETTING_PATH,setting)
    log.info("已保存设置%s:%s"%(key,value))

def get_setting(key):
    return setting.get(key)


if os.path.exists(SETTING_PATH):
    setting = load(SETTING_PATH)


if __name__ == '__main__':
    # set("u","mi")
    print setting
    # save_setting()