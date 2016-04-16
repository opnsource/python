# coding:utf-8
# 线程池
import Queue
import threading


class Threadpool(object):
    def __init__(self, maxThreadSize, maxQueueSize):
        self.maxThreadSize = maxThreadSize
        self.maxQueueSize = maxQueueSize
        self.queue = Queue.Queue(maxQueueSize)
        self.poolQuit = False
        self.poolQuitSaft = False
        Threadpool.__createThread(self)

    def execut(self, argfunc):
        if self.poolQuitSaft:
            return
        item = runItem(argfunc)
        self.queue.put(item)
        pass

    def execut(self, argsfunc, args):
        if self.poolQuitSaft:
            return
        self.queue.put(runItem(argsfunc, args))

    def __createThread(self):
        for i in range(0, self.maxThreadSize):
            t = myThread(self)
            t.start()

    '''
    立刻退出
    '''
    def quitNow(self):
        self.poolQuit = True

    '''
    安全退出
    '''
    def quit(self):
        self.poolQuitSaft = True


class myThread(threading.Thread):
    def __init__(self, out=Threadpool):
        threading.Thread.__init__(self)
        self.queue = out.queue
        self.out = out

    def run(self):
        while True:
            if self.out.poolQuit:
                break
            if self.queue.empty() and self.out.poolQuitSaft:
                break
            item = self.queue.get()
            if item == None:
                continue
            if item.args != None:
                item.func(*item.args)
            else:
                item.func()


class runItem(object):
    def __init__(self, func, args=None):
        self.func = func
        self.args = args


def ____test(i):
    print str(i) + "\n"


if __name__ == '__main__':
    p = Threadpool(5, 1000)
    for i in range(0, 100):
        if i == 65:
            p.quit()
        p.execut(____test, (i,))
