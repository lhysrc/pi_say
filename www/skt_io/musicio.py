from www import socketio
from music import player
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import json
namespace='/music'

import random


@socketio.on('playing_info',namespace=namespace)
def emit_playing_info():
    data = player.playing_info
    emit('playing_info', data)