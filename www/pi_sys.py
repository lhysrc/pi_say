from flask_socketio import SocketIO, emit,send, join_room, leave_room, \
    close_room, rooms, disconnect
from main import pi_sys as pi
from www import socketio
import platform
# from random import randint

thread = None
namespace = '/pisys'



def get_cpuram():
    if "Windows" in platform.uname():
        return None
    cpu_temp = pi.getCPUtemperature()
    cpu_usage = pi.getCPUuse()
    RAM_stats = pi.getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000, 1)
    RAM_used = round(int(RAM_stats[1]) / 1000, 1)
    ran_usage = int(RAM_used / RAM_total * 100)
    return {'cpu_temp': cpu_temp, 'cpu_usage': cpu_usage, 'ram_usage': ran_usage}

def get_diskusage():
    if "Windows" in platform.uname():
        return None
    return pi.getDiskSpace()

def background_thread():
    if "Windows" in platform.uname():
        return
    i,itv = 0,5
    while True:
        socketio.sleep(itv)
        socketio.emit('picpuram',get_cpuram(),namespace=namespace)
        if i == 60:
            socketio.emit('pidisk', get_diskusage(), namespace=namespace)
            i = 0
        i += itv



@socketio.on('getmsg', namespace='/pisys')
def get_pi_sys():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('picpuram', get_cpuram())
    emit('pidisk', get_diskusage())

