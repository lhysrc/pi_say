# coding=utf-8
import logging,platform
import logging.handlers

import sys

log = logging.getLogger()
filename = './log/log'
if __name__ == '__main__':
    filename = '../log/log'
# logging.basicConfig(level=logging.INFO,format='%(name)-6s %(asctime)s | %(levelname)-4s: %(message)s',
#                     datefmt='%a,%y-%m-%d %H:%M:%S',
#                     filename=filename)
#
#formatter = logging.Formatter('%(name)-6s %(asctime)s | %(levelname)-4s: %(message)s', '%a,%y-%m-%d %H:%M:%S',)



formatter = logging.Formatter('%(asctime)s | %(name)s:\n%(levelname)-6s: %(message)s\n', '%a,%y-%m-%d %H:%M:%S',)
"""
# %(name)s                           Logger的名字
# %(levelno)s                        数字形式的日志级别
# %(levelname)s                  文本形式的日志级别
# %(pathname)s                  调用日志输出函数的模块的完整路径名，可能没有
# %(filename)s                     调用日志输出函数的模块的文件名
# %(module)s                       调用日志输出函数的模块名
# %(funcName)s                  调用日志输出函数的函数名
# %(lineno)d                          调用日志输出函数的语句所在的代码行
# %(created)f                         当前时间，用UNIX标准的表示时间的浮点数表示
# %(relativeCreated)d          输出日志信息时的，自Logger创建以来的毫秒数
# %(asctime)s                       字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒
# %(thread)d                          线程ID。可能没有
# %(threadName)s               线程名。可能没有
# %(process)d                       进程ID。可能没有
# %(message)s                    用户输出的消息
"""

def handle_logger(logger,filepath = filename):
    trfhdlr = logging.handlers.RotatingFileHandler(filename, maxBytes=10*1024, backupCount=10)
    # trfhdlr.suffix = ".%Y%m%d"
    trfhdlr.setFormatter(formatter)
    trfhdlr.setLevel(logging.NOTSET)
    log.addHandler(trfhdlr)
    # fhdlr = logging.FileHandler("./tmp/log.log")
    # fhdlr.setFormatter(formatter)
    # fhdlr.setLevel(logging.WARN)
    if 'Windows' in platform.uname():
        stdout_handler = logging.StreamHandler(sys.__stdout__)
        stdout_handler.level = logging.DEBUG
        stdout_handler.formatter = formatter
        log.addHandler(stdout_handler)

    stderr_handler = logging.StreamHandler(sys.__stderr__)
    stderr_handler.level = logging.WARNING
    stderr_handler.formatter = formatter
    log.addHandler(stderr_handler)

    # shdlr = logging.StreamHandler()
    # shdlr.setFormatter(formatter)
    # shdlr.setLevel(logging.INFO)
    # if 'Windows' in platform.uname():
    #     log.addHandler(shdlr)
    log.setLevel(logging.NOTSET)

handle_logger(log)

def info(msg):
    log.info(msg)
def warn(msg):
    log.warn(msg)
def error(msg):
    log.error(msg)


import functools
def func_log(arg):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            words = arg
            if not isinstance(words, (str, int, float)):
                words = 'Called.'
            log.info('Begin Invoke %s: %s' % (func.__name__, words))
            result = func(*args, **kw)
            log.info('End Invoke %s: %s' % (func.__name__, words))
            return result
        return wrapper
    if isinstance(arg, (str, int, float)):
        return decorator
    else:
        return decorator(arg)



@func_log('in de')
def test_a():
    print('a')
@func_log
def test_b(a):
    print('b')

if __name__ == '__main__':
    #print inspect.stack()
    #print(__file__)
    log.debug("debug message")
    log.info("info message")
    log.warn("warn message")
    log.error("error message")
    log.critical("critical message")

    test_a()

    test_b(1)
