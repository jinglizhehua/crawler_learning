import threading
import time
import random

def reading():
    for i in range(10):
        print('reading', i)
        time.sleep(random.randint(1, 2))

# r = threading.Thread(target=reading)
# # r.setDaemon(False)      # 设置线程为后台线程（后台线程不因主线程的结束而结束）默认
# r.setDaemon(True)         # 设置线程为前台线程（主线程结束后子线程也结束）
# r.start()
# print('the end')

def test():
    r = threading.Thread(target=reading)
    r.setDaemon(True)
    r.start()
    print("test end")

# t = threading.Thread(target=test)
# t.setDaemon(False)
# t.start()
# print('The End')
''' 主线程结束后t扔在执行，t结束后r也结束 '''

''' 线程的等待 '''
# t = threading.Thread(target=reading)
# t.setDaemon(False)
# t.start()
# t.join()    # 等待t线程结束
# print("the end")

''' 多线程与资源 '''
# 线程锁 threading.RLock, acquire(), release()
lock = threading.RLock()
words = [5, 1, 3, 7, 9, 6, 4, 2]
def increase():
    global words
    for count in range(5):
        lock.acquire()
        print('A acquired')
        for i in range(len(words)):
            for j in range(i+1, len(words)):
                if words[i] > words[j]:
                    tmp = words[i]
                    words[i] = words[j]
                    words[j] = tmp
        print("A ", words)
        time.sleep(1)
        lock.release()

def decrease():
    global words
    for count in range(5):
        lock.acquire()
        print('D acquired')
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                if words[i] < words[j]:
                    tmp = words[i]
                    words[i] = words[j]
                    words[j] = tmp
        print("D ", words)
        time.sleep(1)
        lock.release()

A = threading.Thread(target=increase)
A.setDaemon(False)
A.start()

# D = threading.Thread(target=decrease)
# D.setDaemon(False)
# D.start()
A = threading.Thread(target=decrease)
A.setDaemon(False)
A.start()

print("the end")



