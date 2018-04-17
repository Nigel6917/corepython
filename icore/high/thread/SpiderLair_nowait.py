# -*- coding: utf-8 -*-
# @Time    : 2017/12/19 
# @Author  : LIYUAN134
# @File    : SpiderLair.py
# @Commment: 爬虫多线程框架
#

import threading
import time
import types
import random

con = threading.Condition()
flag = False


class UrlBox:
    def __init__(self):
        self.MAX_PULL = 2
        self.url_list = []  # 获取爬虫的URL集合

    def addUrls(self, curl):
        if isinstance(curl, str):
            if curl not in self.url_list:
                self.url_list.append(curl)
        elif isinstance(curl, list):
            self.url_list.extend(curl)

    def getUrls(self, gainSize=None):
        if gainSize:
            if gainSize > self.MAX_PULL or gainSize < 0:
                gainSize = self.MAX_PULL
        else:
            gainSize = self.MAX_PULL
        curls = self.url_list[:gainSize]  # 拿走当前库存中url，最多取走500个
        self.url_list = self.url_list[gainSize:]
        return curls

    def getBoxSize(self):
        return len(self.url_list)


def findSinaUrl():
    rtArr = []
    rtArr.append('http://sina1')
    rtArr.append('http://sina1')
    rtArr.append('http://sina1')
    rtArr.append('http://sina1')
    for ii in range(0, random.randint(1, 5)):
        rtArr.append('http://sina1')
    return rtArr


def findSouhuUrl():
    rtArr = []
    # rtArr.append('http://souhu1')
    return rtArr


class Producer(threading.Thread):
    def __init__(self, box, name, maxBox):
        super(Producer, self).__init__()
        self.box = box
        self.name = name
        self.maxBox = maxBox

    def run(self):
        global flag
        print "Producer " + self.name + " Start!\n"
        while True:

            urls1 = findSinaUrl()
            urls2 = findSouhuUrl()

            # print "Producer acquiring the lock " + strings(self.name) + "th time!\n"
            con.acquire()
            # print "Producer acquired the lock " + strings(self.name) + "th time!\n"

            if flag:
                print self.name, "Producer wait\n"
                con.wait()
            else:
                self.box.addUrls(urls1)
                print self.name, "Producer put: ", len(urls1)
                # self.box.addUrls(urls2)
                # print "Producer put: ", len(urls2)
                print self.name, "Producer BOX TOTAL : ", self.box.getBoxSize()
                if self.box.getBoxSize() > self.maxBox:
                    flag = True
                con.notify()
                con.release()
                time.sleep(1)
        print "The End of Producer !"


class Consumer(threading.Thread):
    def __init__(self, box, name, maxBox):
        super(Consumer, self).__init__()
        self.box = box
        self.name = name
        self.maxBox = maxBox

    def run(self):
        global flag
        time.sleep(2)
        print "Consumer " + self.name + " Start!\n"
        while True:
            # print "Producer acquiring the lock " + strings(self.name) + "th time!\n"
            print self.name,'MAIN'
            # con.acquire()
            # print "Producer acquired the lock " + strings(self.name) + "th time!\n"
            rturls = self.box.getUrls()
            if not flag:
                print self.name, "Consumer wait\n"
                # con.wait(1)
                # time.sleep(1)
                flag = True
                con.acquire()
                con.notify()
                con.release()
                # time.sleep(1)
            else:
                print self.name, "Consumer get: ", len(rturls)
                print self.name, "Consumer BOX TOTAL : ", self.box.getBoxSize()
                if self.box.getBoxSize() < 1:
                    flag = False
                # con.notify()
                # con.release()
                time.sleep(2)
        print "The End of Consumer !"


if __name__ == '__main__':
    flag = False
    uBox = UrlBox()
    p = Producer(uBox, "P1", 10)
    c1 = Consumer(uBox, "C1", 10)
    c2 = Consumer(uBox, "C2", 10)
    p.start()
    c1.start()
    c2.start()
    # findSinaUrl()
