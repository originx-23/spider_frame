# 在使用协程池之前, 必须先打猴子补丁.
from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool as BasicPool

class Pool(BasicPool):

    def apply_async(self, func, args=(), kwds={}, callback=None,
            error_callback=None):

        # 为什么协程池中异步任务没有错误回调呢? 协程池只有一个线程. 内部直接就反馈给当前线程.
        # 调用父类中异步任务函数,来执行异步任务
        super().apply_async(func, args=args, kwds=kwds, callback=callback)

    def close(self):
        # 增加一个close方法, 为了和线程池做到统一.
        pass