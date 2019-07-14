# 响应类: 用于封装响应数据
from lxml import etree  # 加入到依赖中
import json
import re

"""
要让该类支持数据解析相关方法
1. xpath 方法, 作用: 使用XPATH来提取html中数据
2. json 方法, 作用: 如果响应是一个json格式字符串, 转换为字典
3. findall方法, 作用; 使用正则来提取数据

"""

class Response(object):

    def __init__(self, url, status_code=200, headers={}, body=None):

        self.url = url # 响应URL
        self.status_code = status_code # 响应状态码
        self.headers = headers # 响应头
        self.body = body # 响应体数据, 二进制数据

    def xpath(self, path):
        """
        使用xpath的路径表达式, 从响应的html文档中提取数据
        :param path: XPATH路径表达式
        :return: lxml的xpath返回的列表
        """
        # 把响应的html转换Element对象
        element = etree.HTML(self.body)
        # 使用element的xpath方法, 来提取数据
        return element.xpath(path)

    def json(self):
        """用于把响应中json格式的字符串, 转换字典
           只有响应内容是json格式的字符串, 才能使用这个方法
        """
        # 如果是python3.6, 可以传入二进制: self.body
        # 如果是python3.5, 只能传入字符串
        return json.loads(self.body.decode())

    def findall(self,pattern, content=None):
        """
        使用正则的findall来提取数据
        :param pattern: 正则表达式
        :param content: 匹配内容; 如果None, 内容就是当前响应的内容
        :return: 返回正则findall匹配的结果
        """

        if content is None:
            # 如果没有传入content,就使用当前响应数据
            content = self.body.decode()
        # 返回正则findall方法, 匹配结果
        return re.findall(pattern, content)

