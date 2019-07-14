
from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item

"""
电影top250,URL规律:
第1页 https://movie.douban.com/top250?start=0&filter=
第2页 https://movie.douban.com/top250?start=25&filter=
第3页 https://movie.douban.com/top250?start=50&filter=
并且一共10页. 

URL规律明显, 并总页数是固定的; 对于这种就可以在一开始就生成所有起始请求

"""

class DoubanSpider(Spider):
    # 豆瓣爬虫名称
    name = 'douban'
    # 由于我们重写了start_requests方法, 所以start_urls属性就可以省略了
    # start_urls = []
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
         # 'Cookie': 'bid=s59SNkBlIjU; ll="118281"; __yadk_uid=KalYHJBq8aLAw6kJrY5QPY2rgoulvelX; _vwo_uuid_v2=DA5E5F698A6E8787A93B0FD4C240B40B2|78767bf0c307e85adbc0839f8617881f; ps=y; ue="583349285@qq.com"; dbcl2="177330829:H6ofbphuYkc"; ck=nuY3; __utmc=30149280; __utmc=223695111; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1539401702%2C%22https%3A%2F%2Fwww.douban.com%2Faccounts%2Flogin%3Fredir%3Dhttps%253A%252F%252Fmovie.douban.com%252Ftop250%253Fstart%253D0%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.258202536.1539221871.1539399302.1539401702.7; __utmz=30149280.1539401702.7.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; __utma=223695111.899287740.1539221871.1539399302.1539401702.7; __utmb=223695111.0.10.1539401702; __utmz=223695111.1539401702.7.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; __utmt=1; __utmv=30149280.17733; __utmb=30149280.2.10.1539401702; _pk_id.100001.4cf6=bc569ece27380a67.1539221871.7.1539401914.1539399301.'
     }

    def start_requests(self):
        # 根据URL规律, 来生成起始URL
        url_pattern = ' https://movie.douban.com/top250?start={}&filter='

        for start in range(0, 250, 25):
            # 生成URL
            url = url_pattern.format(start)
            # 根据URL构建请求
            yield Request(url, headers=self.headers)

    def parse(self, response):
        """解析数据"""
        # 获取包含标题和URL的a标签
        a_s = response.xpath('//div[@class="hd"]/a')
        # 遍历a_s, 获取标题和URL
        for a in a_s:
            item = {}
            item['movie_name'] = a.xpath('./span/text()')[0]
            item['movie_url'] = a.xpath('./@href')[0]

            # yield Item(item)
            # 构建详情页请求, 提取片长
            yield Request(item['movie_url'], callback=self.parse_detail, meta={'item': item}, headers=self.headers)
            """
            为了让框架能够支持这种需求就需要:
            1. 修改Request类, 增加callback和meta成员变量
            2. 修改引擎
            2.1 如果该请求有callback就使用callback来处理响应数据
            2.2 把请求中meta 赋值 响应meta
            """

    def parse_detail(self, response):
        # 解析详情页
        item = response.meta['item']
        # 提取详情页中片长信息
        item['movie_length'] = response.xpath('//span[@property="v:runtime"]/text()')[0]

        return Item(item)
