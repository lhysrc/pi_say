#coding:utf-8
from flask import Flask
from flask_socketio import SocketIO, emit,send, join_room, leave_room, \
    close_room, rooms, disconnect
# from flask.ext.bootstrap import Bootstrap
# try:
#     import signal
#     signal.signal(signal.SIGPIPE, signal.SIG_DFL)
# except: pass
app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)
import pi_sys
#app.debug = True
#
# app.logger_name = 'Flask'
# app.debug_log_format = ('%(name)-6s:%(asctime)s | %(levelname)-4s: %(message)s', '%a,%y-%m-%d %H:%M:%S')
# # app.static_folder='www/static'
# app.logger.setLevel(50)

# 访问记录和socketio的记录只显示warn以上
import logging
logging.getLogger('werkzeug').setLevel(30)
logging.getLogger('engineio').setLevel(30)
logging.getLogger('socketio').setLevel(30)

import views
# bs = Bootstrap(app)

# 模板变量中添加空格，防止与angular js 冲突
app.jinja_env.variable_end_string = ' }}'
app.jinja_env.variable_start_string = '{{ '

def run_app():
    socketio.run(app, host='0.0.0.0',port=3080)
    # app.run(host='0.0.0.0',port=3080,threaded=True)

