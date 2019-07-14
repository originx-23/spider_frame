import logging

# 默认日志等级警告
# 如何设置日志等级呢?
logging.basicConfig(level=logging.DEBUG) # DEBUG
# logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(level=logging.ERROR)


logging.debug("调试信息")
logging.info("普通信息: 用于输出程序运行一些状态信息")
logging.warning("警告信息: 不建议使用方式")
logging.error('错误信息')
logging.critical('严重错误')

# ex = Exception('我出错了')
# logging.exception(ex)

# logging.exception(ex) : 应该使用try...except块
try:
    raise Exception('我错了')
except Exception as ex:
    logging.exception(ex)

