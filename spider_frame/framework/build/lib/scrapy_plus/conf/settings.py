
# 把所有默认配置导入到当前配置文件中
from .default_settings import *

# 导入项目文件夹下的settings
from settings import *

# 注意: 项目文件中settings中必须在默认配置导入之后进行导入.

# import sys
# # print(sys.path)
# for path in sys.path:
#     print(path)

"""
程序时候找文件路径顺序
/Users/itheima/Documents/爬虫项目/day13/code/framework/project_dir
/Users/itheima/Documents/爬虫项目/day13/code/framework
/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python36.zip
/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6
/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/lib-dynload
/Users/itheima/Library/Python/3.6/lib/python/site-packages
/usr/local/lib/python3.6/site-packages
/usr/local/lib/python3.6/site-packages/requests-2.18.4-py3.6.egg
/usr/local/lib/python3.6/site-packages/scrapy_plus-1.0-py3.6.egg
"""