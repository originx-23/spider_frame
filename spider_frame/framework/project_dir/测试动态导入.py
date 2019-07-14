import importlib

# 目录: 根据模块名.类名创建这个类对象
# 类全名: 模块名称.类名
full_name = 'spiders.baidu.BaiduSpider'
# 切割字符串, 获取模块名和类名
# rsplit: 从右向左切割
# maxsplit: 用于指定最多切割多少次
# result = full_name.rsplit('.', maxsplit=1)
# print(result)
# # 模块名(模块路径)
# module_name = result[0]
# # 类名
# class_name = result[1]

# 切割全类名, 获取模块名和类名
module_name, class_name = full_name.rsplit('.', maxsplit=1)

# 根据模块名(模块路径), 导入模块, 获取模块, 该模块中就有这个模块中类
module = importlib.import_module(module_name)
# print(module)
# 使用模块, 通过类名获取类
# getattr: 功能:
#   1. 获取对象中属性的值: 第一个参数是对象, 第二参数就是属性名
#   2. 获取模块中类: 第一个参数是模块, 第二参数就是类名
cls = getattr(module, class_name)
# print(cls)
# 使用类, 来创建实例对象
instance = cls()
print(instance)
print(instance.start_urls)
