# 管道模块; 处理爬虫提取的数据

class Pipeline(object):

    def process_item(self, item, spider):
        # 用于处理item数据
        print(item.data)

        return item