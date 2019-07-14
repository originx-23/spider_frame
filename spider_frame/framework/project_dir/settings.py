
# 设置日志文件
DEFAULT_LOG_FILENAME = 'itcast.log'    # 默认日志文件名称

# 配置开启的爬虫
SPIDERS = [
    # 'spiders.sina.SinaSpider',
    'spiders.baidu.BaiduSpider',
    # 'spiders.douban.DoubanSpider'
]

# 配置管道
PIPELINES = [
    'pipelines.BaiduPipeline',
    # 'pipelines.DoubanPipeline',
]

# # 爬虫中间件
# SPIDER_MIDDLEWARES = [
#     'middlwares.spider_middlewares.SpiderMiddleware1',
#     'middlwares.spider_middlewares.SpiderMiddleware2',
# ]
#
# # 下载器中间件
# DOWNLOADER_MIDDLEWARES = [
#     'middlwares.downloader_middlewares.DownloaderMiddleware1',
#     'middlwares.downloader_middlewares.DownloaderMiddleware2',
# ]

# 配置异步请求数量
ASYNC_COUNT = 10

# 配置异步类型: thread: 线程池版 , coroutine 协程池版
ASYNC_TYPE = 'coroutine'

# 如果是True，那么就是使用分布式，就要使用基于Redis队列和去重容器
# 如果是False, 就不使用分布式,  就使用内存版的队列和去重容器
SCHEDULER_PERSIST = True

# 配置是否要开启断点续爬
# 如果为False就关闭断点续爬
FP_PERSIST = True