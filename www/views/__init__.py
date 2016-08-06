# coding=utf-8
import threading

from flask import render_template,make_response,request,jsonify

from common import util
from main import baidu_tts, play_sound
# from music import ne_music
from www import app

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html',index='index')