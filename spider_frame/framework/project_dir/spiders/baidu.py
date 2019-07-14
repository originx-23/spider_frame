from scrapy_plus.core.spider import Spider

class BaiduSpider(Spider):
    # 爬虫名称
    name = 'baidu'

    # 起始URL
    start_urls = ['http://www.baidu.com', 'http://www.hao123.com', 'http://www.baidu.com']

