import threading
from time import sleep
import random


number:int=0
condition = threading.Condition()
def thread_pool_1():
    while True:
        print("read start while")
        with condition:
            condition.wait()
            print(f"新的数据通知:number now is {number}")


def thread_pool_2():
    global number
    while True:
        i = random.randint(1,10)
        print(f"write thread sleep {i}s")
        sleep(i)
        print("write thread sleep is stop")
        with condition:
            number = number + 1
            condition.notify()




if __name__ == '__main__':
    thread1 = threading.Thread(target=thread_pool_1)
    thread2 = threading.Thread(target=thread_pool_2)
    thread1.start()
    thread2.start()