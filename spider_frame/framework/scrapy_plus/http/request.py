# 请求类: 用于封装请求数据

class Request(object):

    def __init__(self, url, method='GET', headers={}, params={}, data={},
                 callback=None, meta={}, dont_filter=False):

        self.url = url
        self.method = method
        self.headers = headers
        self.params = params # GET请求参数
        self.data = data # POST请求参数

        self.callback = callback # 用于处理请求对应响应数据的解析函数
        self.meta = meta # 用于传递数据

        self.dont_filter = dont_filter # 请求是否需要过滤, 默认是False, 表示要过滤
