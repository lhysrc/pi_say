from www import socketio
from music import player
from flask_socketio import emit
namespace='/music'

import random


@socketio.on('playing_info',namespace=namespace)
def get_playing_info():
    data = player.playing_info
    emit('playing_info', data, namespace=namespace ,broadcast=False)

def emit_playing_info():
    data = player.playing_info
    socketio.emit('playing_info', data, namespace=namespace)