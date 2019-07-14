# Item类: 用于封装爬虫提取出来的数据

class Item(object):

    def __init__(self, data):
        # 使用私有变量, 来记录这个数据
        self.__data = data

    @property # 让这个方法变成一个只读属性. 好处: 保护数据
    def data(self):
        # 返回封装的数据
        return self.__data
