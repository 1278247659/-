# 线程中队列实例


from queue import Queue

# 创建队列
q=Queue(5)
# 存数据
q.put('科比')
q.put('勒布朗')
q.put('JR')
print(q.qsize())#队列大小
q.put('汤普森')
q.put('LOVE')
# q.put('汤姆森',True,3)#如果队列满 程序等待3秒再报错
# True,3 等待三秒再报错
# False 程序直接报错
# 超过5人阻塞队列
print(q.full())#判断队列是否满

# 取数据
print(q.get())
print(q.get())
print(q.get())
print(q.get())
print(q.get())
# 会发现是先进先出
# print(q.get(True,2)) #如若队列空 再取 无结果
print(q.empty())#判断队列是否为空
print(q.qsize())#队列大小