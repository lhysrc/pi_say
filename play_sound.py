#coding:utf-8

def play_by_mp3play(sound_file):
    import mp3play,time
    clip = mp3play.load(sound_file)
    clip.play()
    print "\nStart to play %s" % sound_file
    time.sleep(clip.seconds())
    clip.stop()
    print "Stop"

    # #sound_file = "Should It Matter.mp3"
    # clip = mp3play.load(sound_file)
    # while 1:
    #   if time.localtime().tm_min % 30 == 0:
    #     clip.play()
    #     print "\nStart to play"
    #     time.sleep(clip.seconds())
    #     clip.stop()
    #     print "Stop"
    #   print '>',
    #   time.sleep(30) #暂停30秒（不是30分钟）



#SOUND_FILE = 'test.mp3'
def play_by_pymedia(sound_file):
    file_type = str.split( sound_file, '.' )[ -1 ].lower()
    #1.二进制方法读取前 10000 个字节，保证能读到第一帧音频数据
    f = open( sound_file, 'rb' )
    data= f.read(4096)
    #data= f.read()

    #2.创建合成器对象，解析出最初的几帧音频数据
    import pymedia.muxer as muxer
    dm = muxer.Demuxer(file_type)
    frames = dm.parse( data )
    #print len(frames)

    #3.根据解析出来的 Mp3 编码信息，创建解码器对象
    import pymedia.audio.acodec as acodec
    #dec = acodec.Decoder( dm.streams[ 0 ] )
    #像下面这样也行
    params = {'id': acodec.getCodecID(file_type), 'bitrate': 128000, 'sample_rate': 44100, 'ext': 'mp3', 'channels': 2}
    dec= acodec.Decoder(params)

    if len(frames) > 1:
        #4.解码第一帧音频数据
        frame = frames[0]
        #音频数据在 frame 数组的第二个元素中
        r= dec.decode( frame[ 1 ] )
        print "sample_rate:%s , channels:%s " % (r.sample_rate,r.channels)
        #注意：这一步可以直接解码 r=dec.decode( data)，而不用读出第一帧音频数据
        #但是开始会有一下噪音，如果是网络流纯音频数据，不包含标签信息，则不会出现杂音
    else:
        r=dec.decode(data)

    #5.创建音频输出对象
    import pymedia.audio.sound as sound
    snd = sound.Output( r.sample_rate, r.channels, sound.AFMT_S16_LE )

    #6.播放
    if r: snd.play( r.data )

    #7.继续读取、解码、播放
    while True:
        data = f.read(512)
        if len(data)>0:
            r = dec.decode( data )
            if r: snd.play( r.data )
        else:
            break

    #8.延时，直到播放完毕
    import time
    while snd.isPlaying(): time.sleep( .5 )

#play("./tmp/x.mp3")
#play("./music/xiu_lian_ai_qing.mp3")



if __name__ == '__main__':
    play_by_mp3play(u"C:/Users/linho/Music/Downloads/群星/我是歌手第四季 第2期/修炼爱情.mp3")