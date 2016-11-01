# Memo

### 踩坑记录
- 树莓派上安装eventlet模块需要先安装以下两个包：
    ```
    sudo apt-get install python-dev
    sudo apt-get install libevent-dev
    ```
- 安装上eventlet后歌曲播放结束后socket.io却断开，需要刷新页面才能接收到信息。  
不安装则正常。

- ~~Flask 0.10.1 的jsonify好像有bug, 传了list进去格式化出错。升级到0.11.1正常。~~
- jsonify没问题，是用错了。不能用列表，只能是字典。