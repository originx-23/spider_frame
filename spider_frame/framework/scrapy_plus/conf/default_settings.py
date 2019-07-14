# 用于记录默认配置信息

import logging

# 默认的配置
DEFAULT_LOG_LEVEL = logging.INFO    # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'   # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'log.log'    # 默认日志文件名称


# 配置信息放到模块配置中: 好处: 1. 方便写代码 2.为了增加程序健壮性

# 配置开启的爬虫
SPIDERS = []

# 配置管道
PIPELINES = []

# 爬虫中间件
SPIDER_MIDDLEWARES = []

# 下载器中间件
DOWNLOADER_MIDDLEWARES = []


# 配置异步请求的数量
ASYNC_COUNT = 5

# 配置异步类型: thread: 线程池版 , coroutine 协程池版
ASYNC_TYPE = 'thread'


# scrapy_plus/conf/default_settings.py
# 设置调度器的内容是否要持久化
# 量个值：True和False
# 如果是True，那么就是使用分布式，就要使用基于Redis队列和去重容器
# 如果是False, 就不使用分布式,  就使用内存版的队列和去重容器
SCHEDULER_PERSIST = False

# 是否要开启断点续爬
# 如果是True, 就表示开启断点续爬; 当程序结束了, 我们保留Redis数据中的请求和指纹数据
# 如果是False, 就表示关闭断点续爬, 当前程序结束时候, 就清空Redis数据中的请求和指纹数据
FP_PERSIST = True

# redis默认配置,默认为本机的redis
REDIS_SET_NAME = 'scrapy_plus_fp_set' # fp集合
REDIS_QUEUE_NAME = 'scrapy_plus_request_queue' # request队列
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0