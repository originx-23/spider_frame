# 导入线程池
from multiprocessing.dummy import Pool
import time

# 创建线程池对象
pool = Pool(2)

# 在线程池中调用死循环任务, 就要求线程线程个数必须大于等于任务个数
# def task(msg):
#     while True:
#         print(msg)
#
#
# pool.apply_async(task, args=('任务1', ))
# pool.apply_async(task, args=('任务2', ))
# pool.apply_async(task, args=('任务3', ))

# 通过异步回调函数, 实现死循环效果

def task(msg):
    print(msg)

def task_callback(temp):
    # 再使用异步调用task任务
    pool.apply_async(task, args=('任务1', ), callback=task_callback)
# callback: 当任务完成了 task方法, 执行完毕, 会调用callback指定的函数
pool.apply_async(task, args=('任务1', ), callback=task_callback)


def task_callback2(temp):
    # 再使用异步调用task任务
    pool.apply_async(task, args=('任务2', ), callback=task_callback2)

# callback: 当任务完成了 task方法, 执行完毕, 会调用callback指定的函数
pool.apply_async(task, args=('任务2', ), callback=task_callback2)

def task_callback3(temp):
    # 再使用异步调用task任务
    pool.apply_async(task, args=('任务3', ), callback=task_callback3)

# callback: 当任务完成了 task方法, 执行完毕, 会调用callback指定的函数
pool.apply_async(task, args=('任务3', ), callback=task_callback3)



time.sleep(5)