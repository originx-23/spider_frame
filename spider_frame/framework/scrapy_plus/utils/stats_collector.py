# scrapy_plus/utils/stats_collector.py

import redis
from scrapy_plus.conf.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_SET_NAME

# 如何在框架中使用统计器类来统计信息
# 1. 明确统计东西; 总请求数量, 总响应数量, 重复(过滤)请求数量, 起始请求数量
# 2. 总请求数量,重复(过滤)请求数量 在调度器中进行统计
#    总响应数量, 起始请求数量 在引擎中进行统计的
# 3. 所有统计数据都要使用同一个统计器对象, 来进行统计. 我们在哪里创建统计器对象呢?
#    如果放到调度器中, 统计器如何给引擎呢? 调用器中没有使用引擎
#    引擎: init方法, 创建了调度器, 此时就可以把统计器传递给调度器.


class NormalStatsCollector(object):
    def __init__(self, spider_names=[]):
        #存储请求数量的键
        self.request_nums_key = "_".join(spider_names) + "_request_nums"
        #存储响应数量的键
        self.response_nums_key = "_".join(spider_names) + "_response_nums"
        #存储重复请求的键
        self.repeat_request_nums_key = "_".join(spider_names) + "_repeat_request_nums"
        #存储start_request数量的键
        self.start_request_nums_key = "_".join(spider_names) + "_start_request_nums"

        #初始化收集数据的字典
        self.dict_collector = {
            self.request_nums_key :0,
            self.response_nums_key:0,
            self.repeat_request_nums_key:0,
            self.start_request_nums_key:0
        }

    def incr(self, key):
        self.dict_collector[key] +=1

    def get(self, key):
        return self.dict_collector[key]

    def clear(self):
        del self.dict_collector

    @property
    def request_nums(self):
        '''获取请求数量'''
        return self.get(self.request_nums_key)

    @property
    def response_nums(self):
        '''获取响应数量'''
        return self.get(self.response_nums_key)

    @property
    def repeat_request_nums(self):
        '''获取重复请求数量'''
        return self.get(self.repeat_request_nums_key)

    @property
    def start_request_nums(self):
        '''获取start_request数量'''
        return self.get(self.start_request_nums_key)


class ReidsStatsCollector(object):

    def __init__(self, spider_names=[],
                 host=REDIS_HOST, port=REDIS_PORT,
                 db=REDIS_DB, password=None):
        # Redis数据库, 就是键值类类型数据
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        #存储请求数量的键
        self.request_nums_key = "_".join(spider_names) + "_request_nums"
        #存储响应数量的键
        self.response_nums_key = "_".join(spider_names) + "_response_nums"
        #存储重复请求的键
        self.repeat_request_nums_key = "_".join(spider_names) + "_repeat_request_nums"
        #存储start_request数量的键
        self.start_request_nums_key = "_".join(spider_names) + "_start_request_nums"

    def incr(self, key):
        '''给键对应的值增加1，不存在会自动创建，并且值为1，'''
        self.redis.incr(key)

    def get(self, key):
        '''获取键对应的值，不存在是为0，存在则获取并转化为int类型'''
        ret = self.redis.get(key)
        if not ret:
            ret = 0
        else:
            ret = int(ret)
        return ret

    def clear(self):
        '''程序结束后清空所有的值'''
        self.redis.delete(self.request_nums_key, self.response_nums_key,
                          self.repeat_request_nums_key, self.start_request_nums_key)

    @property
    def request_nums(self):
        '''获取请求数量'''
        return self.get(self.request_nums_key)

    @property
    def response_nums(self):
        '''获取响应数量'''
        return self.get(self.response_nums_key)

    @property
    def repeat_request_nums(self):
        '''获取重复请求数量'''
        return self.get(self.repeat_request_nums_key)

    @property
    def start_request_nums(self):
        '''获取start_request数量'''
        return self.get(self.start_request_nums_key)