#coding:utf-8
from flask import Flask
from flask.ext.bootstrap import Bootstrap
# try:
#     import signal
#     signal.signal(signal.SIGPIPE, signal.SIG_DFL)
# except: pass
app = Flask(__name__)
#app.debug = True
#
# app.logger_name = 'Flask'
# app.debug_log_format = ('%(name)-6s:%(asctime)s | %(levelname)-4s: %(message)s', '%a,%y-%m-%d %H:%M:%S')
# # app.static_folder='www/static'
import views
bs = Bootstrap(app)

def run_app():
    app.run(port=3080,threaded=True)

