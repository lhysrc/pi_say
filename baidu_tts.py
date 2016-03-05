# coding=utf-8
apiKey = "EuWCMZ8mC73R2QimNR5cFkGn"
secretKey = "Yw2wsHC82pPeRCQM5EWjEB263wjDirCU"

auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" \
           + apiKey + "&client_secret=" + secretKey
CUID = "py"
TOKEN = '24.33e501655ef8a7bd71c019a5c174e800.2592000.1459786598.282335-4814376'

import util, os, urllib, urllib2
import play_sound


def refresh_token():
    global TOKEN
    TOKEN = str(util.getJson(auth_url)['access_token'])
    print(TOKEN)


LOCAL_AUDIOS = {
    'NET_ERROR': 'local_audio/net_error.mp3',
    'TTS_ERROR': 'local_audio/tts_error.mp3'
}


def download_tts_file(text, file_name, read_error=False):
    url = "http://tsn.baidu.com/text2audio?lan=zh&cuid=%s&ctp=1&tok=%s&tex=%s" % \
          (CUID, TOKEN, text)
    try:
        request = urllib2.Request(url)
        opener = urllib2.build_opener()
        response = opener.open(request)
        if response.headers['Content-type'] == 'audio/mp3':
            #     refresh_token()
            #     return LOCAL_AUDIOS['TTS_ERROR'] if read_error else download_tts_file(text,file_name,True)
            # else:
            c = response.read()
        else:
            refresh_token()
            return ''
    except urllib2.URLError:
        return LOCAL_AUDIOS['NET_ERROR']
    with open(file_name, "wb") as f:
        f.write(c)
    return file_name


def get_mp3_file(text):
    text = text.strip()
    file_name = "./tmp/%s.mp3" % util.getHashCode(text)
    if os.path.isfile(file_name):
        print "%s已存在，直接播放" % file_name
    else:
        file_name = download_tts_file(text, file_name)
    return file_name


def read_aloud(text):
    mp3_file = get_mp3_file(text)
    retry = 3
    while retry:
        if mp3_file:
            play_sound.play(mp3_file)
            break
        else:
            mp3_file = get_mp3_file(text)
            retry -= 1
    else:
        play_sound.play(LOCAL_AUDIOS['TTS_ERROR'])


if __name__ == '__main__':
    # read_aloud("772距岑村小学还有1站，预计在5分钟后到达")
    import time

    # play_sound.play(LOCAL_AUDIOS['TTS_ERROR'])
    t = time.localtime()
    read_aloud("现在时间是%s点%s分%s秒" % (t.tm_hour, t.tm_min, t.tm_sec))

    pass




# read_aloud("772距岑村小学还有1站，预计在5分钟后到达")
# read_aloud("772距岑村小学还有3站，预计在5分钟后到达")
