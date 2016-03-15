# coding=utf-8
from config import get_baidu_tts_token,set_baidu_tts_token
import logging
log = logging.getLogger(__name__)
apiKey = "EuWCMZ8mC73R2QimNR5cFkGn"
secretKey = "Yw2wsHC82pPeRCQM5EWjEB263wjDirCU"

auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" \
           + apiKey + "&client_secret=" + secretKey
CUID = "py"
TOKEN = get_baidu_tts_token()

import util, os, urllib2, random
import play_sound

def refresh_token():
    global TOKEN
    TOKEN = str(util.getJson(auth_url)['access_token'])
    set_baidu_tts_token(TOKEN)
    log.warn("已刷新百度tts的TOKEN：%s" % TOKEN)


LOCAL_AUDIOS = {
    'NET_ERROR': 'local/net_error.mp3',
    'TTS_ERROR': 'local/tts_error.mp3'
}

import json
def download_tts_file(text, file_name=None, spd=5, pit=5, vol=9, per=0):
    """
    tex
    必填
    合成的文本，使用UTF-8编码，请注意文本长度必须小于1024字节
    lan
    必填
    语言选择,填写zh
    tok
    必填
    开放平台获取到的开发者access_token
    ctp
    必填
    客户端类型选择，web端填写1
    cuid
    必填
    用户唯一标识，用来区分用户，web端参考填写机器mac地址或imei码，长度为60以内
    spd
    选填
    语速，取值0-9，默认为5
    pit
    选填
    音调，取值0-9，默认为5
    vol
    选填
    音量，取值0-9，默认为5
    per
    选填
    发音人选择，取值0-1 ；0为女声，1为男声，默认为女声

    &per=0&vol=9&pit=9&spd=1
    """

    file_name = "./tmp/%s.mp3" % uuid.uuid1() if not file_name else file_name

    url = "http://tsn.baidu.com/text2audio?lan=zh&cuid=%s&ctp=1&tok=%s&tex=%s" % \
          (CUID, TOKEN, text)
    if vol != 5: url += '&vol=%d' % vol
    if spd != 5: url += '&spd=%d' % spd
    if pit != 5: url += '&pit=%d' % pit
    if per != 0: url += '&per=%d' % (per if per == 1 else random.randint(0, 1))
    try:
        request = urllib2.Request(url)
        opener = urllib2.build_opener()
        response = opener.open(request)

        if 'mp3' in response.headers['Content-type']:
            #     refresh_token()
            #     return LOCAL_AUDIOS['TTS_ERROR'] if read_error else download_tts_file(text,file_name,True)
            # else:
            c = response.read()
        elif 'json' in response.headers['Content-type']:
            j = json.load(response)
            log.error('语音转换出错：%s' % j)
            if j['err_no'] == 502:
                refresh_token()
            return ''
        else:
            return ''
    except urllib2.URLError:
        log.error("网络有问题，无法访问：%s" % url)
        return LOCAL_AUDIOS['NET_ERROR']
    with open(file_name, "wb") as f:
        f.write(c)
    return file_name


def get_mp3_file(text, spd=5, pit=5, vol=9, per=0):
    text = text.strip()
    file_name = "./tmp/%s.mp3" % util.getHashCode(text)
    if os.path.isfile(file_name):
        log.info("'%s'的语音文件已存在，直接播放" % text)
    else:
        file_name = download_tts_file(text, file_name, spd, pit, vol, per)
    return file_name


import uuid


def read_aloud(text, cache=False, spd=5, pit=5, vol=9, per=3):
    """
        cache: 缓存语音文件，当然，缓存后，后续参数都失去意义
    """
    # log.INFO("开始播报：%s" % text)
    if cache:
        mp3_file = get_mp3_file(text, spd, pit, vol, per)
    else:
        mp3_file = download_tts_file(text, None, spd, pit, vol, per)
    retry = 3
    while retry:
        if mp3_file:
            play_sound.play(mp3_file)
            break
        else:
            log.warn("语音转换重试。")
            mp3_file = get_mp3_file(text)
            retry -= 1
    else:
        play_sound.play(LOCAL_AUDIOS['TTS_ERROR'])
    if not cache and os.path.exists(mp3_file):
        os.remove(mp3_file)


import functools
def read_text_first(text,cache=False,per=3):
    """
        加上此装饰器则会先播报text再执行该函数
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            read_aloud(text,cache=cache,per=per)
            return func(*args,**kw)
        return wrapper
    return decorator


if __name__ == '__main__':
    # read_aloud("772距岑村小学还有1站，预计在5分钟后到达")
    import time

    # play_sound.play(LOCAL_AUDIOS['TTS_ERROR'])
    t = time.localtime()
    read_aloud("现在时间是%s点%s分%s秒" % (t.tm_hour, t.tm_min, t.tm_sec),per=3)

    pass




# read_aloud("772距岑村小学还有1站，预计在5分钟后到达")
# read_aloud("772距岑村小学还有3站，预计在5分钟后到达")
