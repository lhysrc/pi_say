# 树莓派

 语音报时、报站、天气等应用


树莓派上安装eventlet模块需要先安装以下两个包：
```
sudo apt-get install python-dev
sudo apt-get install libevent-dev
```
安装上eventlet后歌曲播放结束后socket.io却断开，需要刷新页面才能接收到信息。  
不安装则正常。