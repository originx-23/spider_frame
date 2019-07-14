# def parse_requirements(filename):
#     """ load requirements from a pip requirements file """
#     lineiter = (line.strip() for line in open(filename))
#     return [line for line in lineiter if line and not line.startswith("#")]

# for line in open('a.txt'):
#     print(line)

lineiter = (line.strip() for line in open('a.txt'))
# print(lineiter) # <generator object <genexpr> at 0x10a6f84c0>
# for line in lineiter:
#     print(line)
#
lines = [line for line in lineiter if line and not line.startswith("#")]
# print(lines)

from os.path import dirname, join

# with open(join(dirname(__file__), './VERSION.txt'), 'rb') as f:
#     version = f.read().decode('ascii').strip()

# 获取当前文件所在目录绝对路径
print(dirname(__file__)) # /Users/itheima/Documents/爬虫项目/day13/code/framework/test_demo
print(join(dirname(__file__), './VERSION.txt')) # /Users/itheima/Documents/爬虫项目/day13/code/framework/test_demo/./VERSION.txt
