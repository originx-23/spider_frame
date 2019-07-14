# 项目: 管道模块
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider

class BaiduPipeline(object):
    """百度管道, 用于处理百度相关数据"""

    def process_item(self, item, spider):
        """
        处理item函数
        :param item: 爬虫提取到数据
        :param spider: 爬虫对象
        :return: item
        """
        # 通过类型判断数据所属爬虫
        if isinstance(spider, BaiduSpider):
            print('百度数据: {}'.format(item.data))

        return item


class DoubanPipeline(object):
    """豆瓣管道, 用于处理百度相关数据"""

    def process_item(self, item, spider):
        """
        处理item函数
        :param item: 爬虫提取到数据
        :param spider: 爬虫对象
        :return: item
        """
        # 通过类型判断数据所属爬虫
        if isinstance(spider, DoubanSpider):
            print('豆瓣数据: {}'.format(item.data))

        return item

