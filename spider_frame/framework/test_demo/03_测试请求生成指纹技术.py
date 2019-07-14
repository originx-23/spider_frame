from scrapy_plus.http.request import Request
# canonicalize_url: 用于对URL进行规范化处理
from w3lib.url import canonicalize_url
import hashlib

# 一个请求对象中包含方法名称, URL, parmas: get请求参数, data: POST请求参数
# 第一个技术: URL规范化处理
# http://www.baiud.com?name='zhangsan'&age=15
# http://www.baiud.com?age=15&name='zhangsan'
# 上面两个URL对应资源是相同, URL字符串不同, 为了解决这个文件, 就对URL进行规范化处理,也就是对? 后面参数进行排序
url1 = 'http://www.baiud.com?name=zhangsan&age=15'
# url1 = 'http://www.baiud.com?age=15&name=zhangsan'
print(canonicalize_url(url1))

# 请求中使用params 和 data 都是字典参数, 但是字典是乱序
# {'name':'zhangsam', 'age':15}  { 'age':15, 'name':'zhangsam'}
# 第二技术: 对字典进行排序
params = {'name':'zhangsan', 'age': 15}
# params = { 'age': 15, 'name':'zhangsan'}
print(params.items()) # [('name', 'zhangsan'), ('age', 15)]
sorted_params = sorted(params.items(), key=lambda x:x[0])
print(sorted_params)

# 第三个技术: hashlib.sha1 算法
# 获取一个sha1算法对象
url = 'http://www.baiud.com?name=zhangsan&age=15'
sha1 = hashlib.sha1()

# update只支持二进制数据, 不支持字符串
sha1.update(url1.encode('utf8'))
# 把数据生成一个指纹字符
print(sha1.hexdigest()) # 36db7602cb75ff39cb2e931f8fd598c2b79e9034

import six

# 第四个技术: 无论是python2 还是python3 都可以生成二进制数据
def str_to_bytes(s):
    if six.PY3:
        # 如果是python3: str类型: Unicode的字符串, bytes类型: 二进制
        return s.encode('utf8') if isinstance(s, str) else s
    else:
        # 如果是python2: str类型: 是二进制数据, unicode类型: 是字符串;
        # python2: 默认编码方式 ASCII码, 所以此处必须指定
        return s if isinstance(s, str) else s.encode('utf8')

print(str_to_bytes('哈哈'))
print(str_to_bytes(b'abc'))

