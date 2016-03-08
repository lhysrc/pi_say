# coding=utf-8
import logging
import logging.handlers
log = logging.getLogger()

#formatter = logging.Formatter('%(name)-6s %(asctime)s | %(levelname)-4s: %(message)s', '%a,%y-%m-%d %H:%M:%S',)
formatter = logging.Formatter('%(asctime)s | %(levelname)-4s: %(message)s', '%a,%y-%m-%d %H:%M:%S',)
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



trfhdlr = logging.handlers.TimedRotatingFileHandler('./log/log','s',1,7)
trfhdlr.suffix = "%Y%m%d.log"
trfhdlr.setFormatter(formatter)


# fhdlr = logging.FileHandler("./tmp/log.log")
# fhdlr.setFormatter(formatter)
# fhdlr.setLevel(logging.WARN)

shdlr = logging.StreamHandler()
shdlr.setFormatter(formatter)


log.addHandler(trfhdlr)
log.addHandler(shdlr)
log.setLevel(logging.NOTSET)


def INFO(msg):
    log.info(msg)
def WARN(msg):
    log.warn(msg)
def ERROR(msg):
    log.warn(msg)

if __name__ == '__main__':
    log.debug("debug message")
    log.info("info message")
    log.warn("warn message")
    log.error("error message")
    log.critical("critical message")