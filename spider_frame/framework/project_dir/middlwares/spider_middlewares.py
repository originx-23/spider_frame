# 爬虫模块: 用于对请求和响应数据进行预处理

class SpiderMiddleware1(object):

    def process_request(self, request):
        # 用于处理请求的: 在请求对象交给引擎之前调用
        print("SpiderMiddleware1-process_request-{}".format(request.url))

        return request

    def process_response(self, response):
        # 用于处理响应数据: 在响应对象交给爬虫之前调用
        print("SpiderMiddleware1-process_response-{}".format(response.url))
        return response


class SpiderMiddleware2(object):

    def process_request(self, request):
        # 用于处理请求的: 在请求对象交给引擎之前调用
        print("SpiderMiddleware2-process_request-{}".format(request.url))

        return request

    def process_response(self, response):
        # 用于处理响应数据: 在响应对象交给爬虫之前调用
        print("SpiderMiddleware2-process_response-{}".format(response.url))
        return response
