# six: 是一个第三方模块, 专门用于处理python2和python3兼容
# six安装: pip3 install six

from ..conf import settings

if settings.SCHEDULER_PERSIST:
    # 如果使用分布式, 我们就要使用基于Redis队列和去重容器
    from ..utils.queue import Queue
    from ..utils.set import RedisFilterContainer as FilterContainer
else:
    # 如果不使用分布式, 就导入内存把队列和去重容器
    from six.moves.queue import Queue
    from ..utils.set import NoramlFilterContainer as FilterContainer


from w3lib.url import canonicalize_url # 加入依赖: requirements.txt
import hashlib
import six
from ..utils.log import logger


# 调度器模块: 1. 缓存请求 2. 请求去重
class Scheduler(object):

    def __init__(self, stats_collector):
        # 创建队列, 用于缓存请求对象
        self.queue = Queue()
        # 创建一个去重容器: 使用set集合
        self.filter_container = FilterContainer()
        # 接收引擎传递过来统计器对象
        # 用于统计总请求数量和重复的请求数量
        self.stats_collector = stats_collector

    def clear(self):
        # 如果是分布时候, 清空请求队列和指纹容器
        if settings.SCHEDULER_PERSIST:
            # 清空请求队列
            self.queue.clear()
            # 清空指纹容器
            self.filter_container.clear()

    def add_request(self, request):

        # 如果该请求需要被过滤 并且 重复了, 才过滤该请求
        if not request.dont_filter and self.filter_request(request):
            # 统计被过滤掉请求数量
            # 让统计器中repeat_request_nums_key对应值增加1
            self.stats_collector.incr(self.stats_collector.repeat_request_nums_key)

            # 如果请求已经存在, 就不在入队了
            return

        # 如果dont_filter为true就会直接入队
        # 如果来到这里, 说明该请求不重复.
        # 把请求对象, 添加到队列中
        self.queue.put(request)
        # 每次添加一个请求, 到队列中, 就让请求总数量增加1
        self.stats_collector.incr(self.stats_collector.request_nums_key)

    def get_request(self):
        # 从队列中, 取出请求对象, 并返回
        return self.queue.get()

    def filter_request(self, request):
        # 实现请求去重, 如果该请求需要过滤就返回True, 否则返回False
        # 1. 把请求对象生成一个指纹
        fp = self.__gen_fp(request)
        # 2. 如果指纹fp, 在去重容器中, 说明该请求已经存在了, 此时返回True
        if self.filter_container.exists(fp):
            logger.info("被过滤掉请求: {}".format(request.url))
            return True
        # 3. 如果代码能来到这里, 说明这个指纹在指纹容器中不存在
        # 把该指纹添加到指纹容器中
        self.filter_container.add_fp(fp)

        # 返回False, 说明该请求是一个全新请求
        return False


    def __gen_fp(self, request):
        """
        把请求对象生成一个指纹字符串
        :param request: 请求对象
        :return: 指纹字符串
        """
        # 1. 请求方法
        method = request.method.upper()
        # 2. 请求的URL, 对URL进行规范化处理
        url = canonicalize_url(request.url)
        # 3. 请求参数: params, 对字典参数进行排序
        params = sorted(request.params.items(), key=lambda x:x[0])
        # 4. 请求体
        data = sorted(request.data.items(), key=lambda x: x[0])

        # 创建sha1算法对象
        sha1 = hashlib.sha1()
        # 向sha1算法中添加需要生成指纹的数据
        # 把方法名添加到sha1算法中
        sha1.update(self.__str_to_bytes(method))
        # 把请求的URL, 添加到sha1算法中
        sha1.update(self.__str_to_bytes(url))
        # 把请求的params参数, 添加到sha1算法中
        sha1.update(self.__str_to_bytes(str(params)))
        # 把请求的data, 添加到sha1算法中
        sha1.update(self.__str_to_bytes(str(data)))

        # 使用sha1算法中数据, 生成一个指纹字符串
        return  sha1.hexdigest()


    def __str_to_bytes(self, s):
        if six.PY3:
            # 如果是python3: str类型: Unicode的字符串, bytes类型: 二进制
            return s.encode('utf8') if isinstance(s, str) else s
        else:
            # 如果是python2: str类型: 是二进制数据, unicode类型: 是字符串;
            # python2: 默认编码方式 ASCII码, 所以此处必须指定
            return s if isinstance(s, str) else s.encode('utf8')
