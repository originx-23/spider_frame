# 用于启动测试爬虫框架
from scrapy_plus.core.engine import Engine

if __name__ == '__main__':

    # 创建引擎对象
    engine = Engine()
    # 启动引擎
    engine.start()
