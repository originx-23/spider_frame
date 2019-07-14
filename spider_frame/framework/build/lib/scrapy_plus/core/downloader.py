import requests
from ..http.response import Response
# 下载器模块: 用于发送请求, 获取响应数据

class Downloader(object):

    def get_response(self, request):
        # 根据请求获取响应数据
        # 使用requests模块来发送请求
        if request.method.upper() == 'GET':
            # 如果是GET请求, 就使用requests,发送get请求
            resp = requests.get(request.url, headers=request.headers, params=request.params)
        elif request.method.upper() == 'POST':
            resp = requests.post(request.url, headers=request.headers, data=request.data)
        else:
            raise Exception('暂时支持GET和POST请求')

        # 把resp封装为响应对象返回
        return Response(resp.url,
                        status_code=resp.status_code,
                        headers=resp.headers,
                        body=resp.content)