
from ..http.request import Request
from ..item import Item
# 爬虫模块: 1. 构建起始请求 2. 解析响应数据

class Spider(object):

    # 爬虫名称
    name = 'spider'

    # 起始URL
    start_urls = []

    def start_requests(self):
        # 由于这个方法, 变成了生成器, 那么调用这个方法地方就做相应修改
        # 哪里调用方法: 引擎
        for url in self.start_urls:
            # 把起始URL, 封装请求对象,
            # 如果使用return只能返回第一个请求对象
            # 使用yield让方法变成一个生成器.
            yield Request(url)

    def parse(self, response):
        # 解析响应数据
        print(response.url)
        # 创建Item对象, 用于封装提取的数据
        return Item(response.body)

