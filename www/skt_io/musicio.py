from www import socketio
from music import player
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import json
namespace='/music'

import random


@socketio.on('playing_info',namespace=namespace)
def emit_playing_info():
    ret = {
        'song_name': player.get_playing_song().file_name if player.playing_flag else None,
        'vol'      : player.playing_volume,
        'pause'    : player.pause_flag,
        'playing'  : player.playing_flag
    }
    emit('playing_info', ret)