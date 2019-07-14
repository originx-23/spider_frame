# 导入配置文件
from ..conf import settings

if settings.ASYNC_TYPE.lower() == 'thread':
    # 导入线程池
    from multiprocessing.dummy import Pool
else:
    # 导入协程池
    # 猴子补丁必须在requests模块之前打
    from ..async.coroutine import Pool


from .scheduler import Scheduler
from .downloader import Downloader
from ..http.request import Request

# 导入日志对象
from ..utils.log import logger
from datetime import datetime

from collections import Iterable

import importlib

import time


# 1. 如果分布式就导入基于Redis统计器, 否则就导入内存版的统计器
if settings.SCHEDULER_PERSIST:
    from ..utils.stats_collector import ReidsStatsCollector as StatsCollector
else:
    from ..utils.stats_collector import NormalStatsCollector as StatsCollector


# 引擎模块: 1. 负责各模块之间调度 2. 各个模块间数据传递
"""
思路:
 1. 创建各个模块的对象, 在init方法
 2. 提供一个对外请求引擎的方法(start)
 3. 提供一个私有的启动引擎的方法, 用于实现核心逻辑
 
让引擎支持多管道
1. 修改init方法, 接收管道列表参数
2. 修改原来self.pipeline位置, 改为遍历self.pipelines, 使用每一个pipeline数据进行处理

让引擎支持多中间件
1. 修改init方法, 接收爬虫中间件列表 和 下载器中间件列表
2. 修改原来self.spider_middleware的地方, 改为遍历self.spider_middlewares每一个爬虫中间件调用响应方法
2. 修改原来self.downloader_middleware的地方, 改为遍历self.downloader_middleware每一个下载器中间件调用响应方法

实现通过配置文件, 动态导入爬虫, 管道, 下载器中间件, 爬虫中间件
1. 实现根据配置列表, 动态导入的方法
2. 在init方法中调用该方法, 创建爬虫, 管道, 下载器中间件, 爬虫中间件

实现线程池版异步爬虫:
1. 创建线程池对象, 在init方法
2. 在__start方法中, 使用异步来执行__add_start_requests和__execute_request_response_item
3. 通过异步回调来使用_execute_request_response_item死循环. 

解决在分布式情况下, 结束条件的问题
1. 如果分布式就导入基于Redis统计器, 否则就导入内存版的统计器
2. 在init方法中, 创建统计器对象
3. 把统计器对象通过init方法, 传入到调度器中
4. 调度器中使用统计器, 统计总请求数量, 和重复(被过滤掉)请求数量
5. 在引擎中, 使用统计器, 统计总响应数量和起始请求的数量
6. 结束条件, 就是统计器请求数量和响应数量进行比较

"""
class Engine(object):

    def __init__(self):

        #  1. 创建各个模块的对象,
        self.spiders = self.__auto_import(settings.SPIDERS, is_spider=True)

        # 2. 在init方法中, 创建统计器对象
        self.stats_collector = StatsCollector(self.spiders.keys())
        # 3. 把统计器对象通过init方法, 传入到调度器中
        self.scheduler = Scheduler(self.stats_collector)

        self.downloader = Downloader()
        self.pipelines = self.__auto_import(settings.PIPELINES)

        # 初始化爬虫中间件和下载器中间件
        # 1. 修改init方法, 接收爬虫中间件列表 和 下载器中间件列表
        self.spider_middlewares = self.__auto_import(settings.SPIDER_MIDDLEWARES)
        self.downloader_middlewares = self.__auto_import(settings.DOWNLOADER_MIDDLEWARES)

        # 定义变量, 用于统计总响应数量
        # self.total_response_count = 0

        # 1. 创建线程池对象, 在init方法
        self.pool = Pool()
        # 定义变量, 用于统计起始请求已经结束爬虫数量
        self.start_requests_finished_spider_count = 0


    def __auto_import(self, full_names, is_spider=False):
        """
        根据全类名列表, 创建类对象, 添加到容器中进行返回
        :param full_names: 全类名列表
        :param is_spider:  是不是爬虫, 如果是爬虫返回字典, 否则就返回列表
        :return: 如果是爬虫返回字典, 否则就返回列表
        """
        # 定义变量, 用于存储返回的结果
        # 如果是爬虫, 就是字典, 否则就列表
        instances = {} if is_spider else []

        # 变量full_name, 获取每一个类的全名, 根据全名创建对象, 添加结果集中
        for full_name in full_names:
            # 获取模块名和类名
            module_name, class_name = full_name.rsplit('.', maxsplit=1)
            # 通过模块名, 导入模块
            module = importlib.import_module(module_name)
            # 通过类名, 从模块中取出该类
            cls = getattr(module, class_name)
            # 通过类创建对象
            instance = cls()
            # 把对象存储结果集中
            if is_spider:
                # instance.name: 爬虫名称
                # instance: 爬虫对象
                instances[instance.name] = instance
            else:
                instances.append(instance)

        # 返回对象结果: 如果是爬虫返回是爬虫字典, 其他返回时对象列表
        return instances





    def start(self):
        # 对外提供启动引擎的方法
        # 启动时间
        start = datetime.now()
        logger.info("启动时间: {}".format(start))
        self.__start()
        end = datetime.now()
        logger.info("总请求数量: {}".format(self.stats_collector.request_nums))
        logger.info("起始请求数量: {}".format(self.stats_collector.start_request_nums))
        logger.info("被过滤掉请求数量: {}".format(self.stats_collector.repeat_request_nums))
        logger.info("总响应处理数量: {}".format(self.stats_collector.response_nums))

        logger.info("结束时间: {}".format(end))
        logger.info("总耗时: {}秒".format((end-start).total_seconds()))

        # 如果开启分布式, 在程序结束时候, 请求统计信息
        if settings.SCHEDULER_PERSIST:
            self.stats_collector.clear()
            # 如果 FP_PERSIST 是True, 就表示开启断点续爬; 当程序结束了, 我们保留Redis数据中的请求和指纹数据
            # 如果FP_PERSIST 是False, 就表示关闭断点续爬, 当前程序结束时候, 就清空Redis数据中的请求和指纹数据
            if not settings.FP_PERSIST:
                # 清空调度器中, 请求队列和指纹容器
                self.scheduler.clear()



    def __error_callback(self, ex):
        # 使用日志模块记录错误信息
        try:
            raise ex
        except Exception as e:
            logger.exception(e)


    def __execute_callback(self, temp):
        # 循环回调, 从而实现不断调用__execute_request_response_item
        self.pool.apply_async(self.__execute_request_response_item, callback=self.__execute_callback,
                              error_callback=self.__error_callback)

    def __start(self):
        # 用于实现启动引擎核心逻辑

        # 2. 在__start方法中, 使用异步来执行__add_start_requests和__execute_request_response_item
        # 1. 添加起始请求到调度器中
        self.pool.apply_async(self.__add_start_requests, error_callback=self.__error_callback)

        # 实现多异步任务
        for i in range(settings.ASYNC_COUNT):
            # 3. 通过异步回调来使用_execute_request_response_item死循环.
            # 2. 用于处理请求, 响应和Item数据的
            # error_callback: 当调用异步任务内部出错了, 就调用error_callback所指定函数
            self.pool.apply_async(self.__execute_request_response_item, callback=self.__execute_callback,
                                  error_callback=self.__error_callback)

        # 等待异步任务能够开始执行
        time.sleep(0.1)

        while True:
            # 在我们去判断结束条件之前, 等待一下, 从而提高CPU使用效率
            time.sleep(0.1)

            # 如果还有爬虫起始请求还没有走完, 就让程序继续等待
            if self.start_requests_finished_spider_count < len(self.spiders):
                # 跳过本次循环continue后面语言, 继续下一次循环
                continue

            # 3. 退出请求: 条件: 所有请求都处理完了
            # 统计请求总数量 和响应处理的总数量, 如果响应处理的总数量 >= 请求的总数量, 就可以退出了
            # 在哪里统计请求总数量: 由于所有请求都要添加到队列中, 所以在调度器的add_request方法, 中可以统计
            # 在哪里响应处理的总数量: 由于 __execute_request_response_item 是处理响应的, 所可以该方法中进行统计
            # 使用统计器中响应数量和请求数量进行比较
            if self.stats_collector.response_nums >= self.stats_collector.request_nums:
                # 如果响应处理的总数量 >= 请求的总数量, 就可以退出了
                break


    def __execute_request_response_item(self):
        """用于处理请求, 响应和Item数据的"""

        # 1 / 0 # 此处会报错

        # 调用调度器get_request方法, 获取请求对象
        request = self.scheduler.get_request()

        # 获取该请求对应爬虫对象
        spider = self.spiders[request.spider_name]

        for downloader_middleware in self.downloader_middlewares:
            # 调用下载器中间件的process_request方法, 对请求进行处理
            request = downloader_middleware.process_request(request)

        # 调用下载器get_response方法,根据请求获取响应数据
        response = self.downloader.get_response(request)

        #  2.2 把请求中meta 赋值 响应meta
        response.meta = request.meta

        for downloader_middleware in self.downloader_middlewares:
            # 调用下载器中间件的process_response方法, 对响应进行处理
            response = downloader_middleware.process_response(response)

        # 调用爬虫中间件的process_response方法, 对响应进行处理
        for spider_middleware in self.spider_middlewares:
            response = spider_middleware.process_response(response)
        # 调用爬虫parse函数, 传入response, 获取解析数据
        # 处理解析函数, 返回多结果
        #  2.1 如果该请求有callback就使用callback来处理响应数据
        if request.callback :
            results = request.callback(response)
        else:
            # 如果请求没有callback就使用爬虫parse函数进行处理
            results = spider.parse(response)

        # 判断当前结果,是否是可以迭代的, 如果不是把它变为可迭代的
        if not isinstance(results, Iterable):
            results = [results]

        # 来到这里results一定可以迭代的
        for result in results:
            if isinstance(result, Request):
                # 调用爬虫中间件process_request方法, 对请求进行处理
                for spider_middleware in self.spider_middlewares:
                    result = spider_middleware.process_request(result)

                # 给result这个请求指定爬虫名称
                result.spider_name = spider.name

                # 如果解析结果是一个请求对象, 就把这个请求添加到调度器中
                self.scheduler.add_request(result)
            else:
                # 如果不是请求, 我们就认为出来的数据
                # 就调用pipeline的process_item方法进行处理
                for pipeline in self.pipelines:
                    result = pipeline.process_item(result, spider)

        # 每次处理完成一个响应, 就让变量增加1
        self.stats_collector.incr(self.stats_collector.response_nums_key)

    def __add_one_spider_start_requests_callback(self, temp):
        # 每完成要给起始请求, 就该变量增加1
        self.start_requests_finished_spider_count += 1

    def __add_start_requests(self):
        """添加起始请求, 到调度器中"""
        # 调用爬虫的start_requests方法, 获取起始请求对象
        # 由于现在start_requests是一个生成器, 所以要进行遍历

        for spider_name,spider in self.spiders.items():
            # self.__add_one_spider_start_requests(spider, spider_name)
            # 使用异步调用该方法
            self.pool.apply_async(self.__add_one_spider_start_requests,
                                  args=(spider, spider_name),
                                  callback=self.__add_one_spider_start_requests_callback)


    def __add_one_spider_start_requests(self, spider, spider_name):
        """添加一个爬虫的起始请求到调度器中"""
        for request in spider.start_requests():
            # 设置该请求对应的爬虫名称
            request.spider_name = spider_name

            # 调用爬虫中间的process_request来处理请求
            for spider_middleware in self.spider_middlewares:
                request = spider_middleware.process_request(request)
            # 调用调度器的add_request, 把请求添加到调度器中
            self.scheduler.add_request(request)
            # 使用统计器类统计起始请求的数量
            self.stats_collector.incr(self.stats_collector.start_request_nums_key)

