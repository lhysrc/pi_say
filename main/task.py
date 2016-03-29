# coding=utf-8
# 播放本地音乐
# 播放网络音乐
# 报站
# 播报语音：天气
# 自动签到（无需自定义）

import play_sound,ne_music,gz_bus,baidu_tts
tasks = {
    "播放本地音乐":play_sound.play_local_music,
    "播放网络音乐":ne_music.play_a_list,
    "报站":gz_bus.baozhan,
    "播报天气":0,
    "播报语音":baidu_tts.read_aloud,

}