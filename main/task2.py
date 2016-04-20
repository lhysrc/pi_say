# coding=utf-8
import uuid

import config
import itertools,json
tasks = []
def music():pass
def tell_bus():pass
def tell_weather():pass
def read_text():pass
MUSIC,TELL_BUS,TELL_WEATHER,READ_TEXT = 'music','tell_bus','tell_weather','read_text'
task_types = {
    MUSIC       : music,
    TELL_BUS    : tell_bus,
    TELL_WEATHER: tell_weather,
    READ_TEXT   : read_text
}

class Task(object):
    def __init__(self, hour, min, task_type_or_func,args=(), workday=False,holiday=False, pause_days=0):
        self.id = str(uuid.uuid4())
        self.task_type_or_func = task_type_or_func
        self.args = tuple(args)
        self.hour = hour
        self.min = min
        self.workday = workday
        self.holiday = holiday
        self.pause_days = pause_days

    def __repr__(self):
         return str(self.__dict__) if self.task_type_or_func in task_types else '<PreTask>'

    def to_dict(self):
        if self.task_type_or_func not in task_types:return None
        d = self.__dict__.copy()
        del d['id']
        return d


def load_all_tasks():
    for tp in task_types:
        d = config.get('Task',tp)
        if d:
            j = json.loads(d)
            for t in j:
                tasks.append(Task(**t))
    #todo: log

def save_all_tasks():
    for k,g in itertools.groupby(tasks,key=lambda t:t.task_type_or_func):
        if k in task_types:
            g = map(lambda t:t.to_dict(),g)
            config.set('Task', k, json.dumps(g))
    config.save()

# def save_task(task):
#     if task.task_type_or_func not in task_types: return # todo 分任务类型存？任务不多没必要
#     name = task.task_type_or_func
#     task_to_save
#     config.set("Task",name,task)
#     config.save()

if __name__ == '__main__':

    load_all_tasks()

    # tasks += [Task(7, 47, TELL_BUS, (581, "长兴路东", 162545), workday=True),
    #           Task(8, 5, TELL_BUS, (498, "长兴路东", 261508), workday=True),
    #           Task(7, 47, TELL_BUS, ('b11', "长兴路东", 87792), workday=True),
    #           Task(7, 35, MUSIC, (), workday=True),
    #           Task( 10, 0, MUSIC, (), holiday=False),
    #           Task( 22, 49, MUSIC, (), workday=True, holiday=False,pause_days=3),
    #           Task(9,0,max,())
    # ]

    # save_all_tasks()

    from threading import Timer
    import time


    t = time.localtime()
    task_changed = False
    for task in tasks:
        if t.tm_hour == task.hour and task.min >= t.tm_min:
            func = task_types[task.task_type_or_func] \
                if task.task_type_or_func in task_types else task.task_type_or_func
            if task.pause_days == 0:
                interval = (task.min - t.tm_min) * 60 - t.tm_sec
                interval = max(0, interval)
                print(u"将在%s秒后执行任务：%s。|%s。" % (interval, func.__name__,task))
                Timer(interval, func, task.args).start()
            elif task.pause_days > 0:
                task.pause_days -= 1
                task_changed = True
                print(u"今日不执行任务‘%s’，将于%s日后执行。|%s。" % (func.__name__, task.pause_days,task))
    if task_changed: save_all_tasks()