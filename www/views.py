from www import app
import baidu_tts
@app.route('/')
def index():
    return "Hello, World!"

# @app.route('/wx', methods = ['GET', 'POST'] )
# def wx():
#     from WeiXinCore.WeiXin import check_signature,echo
#     from flask import request
#     if not check_signature(request.args) and not app.debug:
#         return ""
#     return echo

@app.route('/tts/<name>')
def tts_page(name):
    baidu_tts.read_aloud(name)
    return name

# @app.route('/tts',methods='post')
# def tts():
#     baidu_tts.read_aloud("123")