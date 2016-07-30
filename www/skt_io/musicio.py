from www import socketio
from music import player

namespace='/music'

import random


@socketio.on('playing_info',namespace=namespace)
def get_playing_info():
    emit_playing_info()

def emit_playing_info():
    data = player.playing_info
    socketio.emit('playing_info', data, namespace=namespace)