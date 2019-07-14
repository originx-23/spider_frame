from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
import time

class SinaSpider(Spider):

    name = 'sina'

    def start_requests(self):

        # 准备URL
        url = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php'
        # 请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Referer': 'http://roll.news.sina.com.cn/s/channel.php?ch=01'
        }

        while True:
            # 构建请求
            # 默认所有请求只要重复了, 就会过滤掉
            # 如果请求指定了dont_filter=True,该请求就不过滤
            # 1. 修改框架中Request, 接收dont_filter
            # 2. 修改框架中调度器, 添加请求的时候, 判断这个请求是否需要过滤
            yield Request(url, headers=headers, dont_filter=True)
            # 休息一下: 一定要yield后面, 协程切换后才睡, 否则到程序卡该位置
            time.sleep(2)
            # 问题: 当起始请求等待时间比较长时候, 起始请求还没有执行完程序就结束了
            # 解决: 让程序等待到所有爬虫start_reqeusts方法都走完了, 才去爬虫是否应该结束.


