#coding=utf-8
import util,os
cuid ="py"
def get_token():
    token = "24.5b307450afcd66680a018cf35228224c.2592000.1459040998.282335-4814376"
    return token


def get_mp3_file(text):
    text = text.strip()
    file_name = "./tmp/%s.mp3" % util.getHashCode(text)
    if os.path.isfile(file_name):
        print "%s已存在，直接播放" % file_name
    else:
        url = "http://tsn.baidu.com/text2audio?lan=zh&cuid=%s&ctp=1&tok=%s&tex=%s" % (cuid,get_token(),text)
        c = util.getContent(url)
        with open(file_name,"wb") as f:
            f.write(c)
    return file_name



def read_aloud(text):
    mp3_file = get_mp3_file(text)
    import platform,os,play_sound
    if "Windows" in platform.uname():
        play_sound.play(mp3_file)
    else:
        os.system("mpg123 -q " + mp3_file)

#read_aloud("772距岑村小学还有1站，预计在5分钟后到达")
#read_aloud("772距岑村小学还有3站，预计在5分钟后到达")
