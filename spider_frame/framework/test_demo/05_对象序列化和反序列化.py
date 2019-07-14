from scrapy_plus.http.request import Request
import pickle

# 创建Request对象
request = Request('http://www.baidu.com')

# 在把数据存储到Redis数据库之前, 需要对对象进行序列化
# Redis不能直接存储Python对象, 可以存储二进制
# 序列化: 把对象转换为二进制信息
b = pickle.dumps(request)
# 将来我们会使用这个二进制数据存储到Redis数据库中
print(b)
# 将来从Redis数据库中取出请求的二进制数据, 还要还原为request
# 反序列: 把二进制数据转换为对象
new_request = pickle.loads(b)
print(new_request)
print(new_request.url)



