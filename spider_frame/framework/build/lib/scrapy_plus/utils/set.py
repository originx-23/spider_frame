# scrapy_plus/utils/set.py
# 实现去重容器:
#   内存版去重容器
#   Redis版去重容器

import redis
from scrapy_plus.conf import settings

# 用于定义接口, 去重容器中应该具有什么样的方法.
class BaseFilterContainer(object):

    def add_fp(self, fp):
        '''往去重容器添加一个指纹'''
        pass

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        pass

class NoramlFilterContainer(BaseFilterContainer):
    '''利用python的集合类型'''

    def __init__(self):
        self._filter_container = set()

    def add_fp(self, fp):
        ''''''
        self._filter_container.add(fp)

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        if fp in self._filter_container:
            return True
        else:
            return False

class RedisFilterContainer(BaseFilterContainer):
    '''利用redis的指纹集合'''
    REDIS_SET_NAME = settings.REDIS_SET_NAME
    REDIS_SET_HOST = settings.REDIS_HOST
    REDIS_SET_PORT = settings.REDIS_PORT
    REDIS_SET_DB = settings.REDIS_DB

    def __init__(self):
        self._redis = redis.StrictRedis(host=self.REDIS_SET_HOST, port=self.REDIS_SET_PORT ,db=self.REDIS_SET_DB)
        self._name = self.REDIS_SET_NAME

    def add_fp(self, fp):
        '''往去重容器添加一个指纹'''
        self._redis.sadd(self._name, fp)

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        return self._redis.sismember(self._name, fp) # 如果存储就返回True, 否则就返回False

    def clear(self):
        # 清空Redis指纹中数据
        self._redis.delete(self._name)