#-*- coding:utf-8 -*-
#
# @author EndangeredFish <zwy346545141@gmail.com>   LucienShui <lucienshui.outlook.com>    hamburger
# @Date 12.23.2017
import requests
import re
import queue
import threading
import time
from pprint import pprint as pp

# 登陆地址
urllogin = 'http://exam.upc.edu.cn/login.php'
# 榜单地址
urlstatus = "http://exam.upc.edu.cn/status.php?problem_id=&user_id=&language=-1&jresult=4"
# 登录信息
data = {"user_id": "summer17016", "password": "sqy201309"}
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
           "Accept-Encoding": "gzip",
           "Accept-Language": "zh-CN,zh;q=0.8",
           "Referer": "http://exam.upc.edu.cn/",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
           }
# 正则表达式
pattern = "<tr class='(even|odd)row'><td>([0-9]+)</td><td><a href='userinfo\.php\?user=([a-zA-Z0-9_]+)'>([a-zA-Z0-9_]+)</a></td><td><div class=center><a href='problem\.php\?id=(\d+)'>(\d+)</a></div></td><td><span class='btn btn-success'>(\*?)正确</span>"


def producer(out_q,data):
    while True:
        out_q.put(data)


def login():
    reslogin = requests.post(urllogin, data=data, headers=headers)
    return reslogin.cookies


def getstatus(cookies_):
    responstatus = requests.get(urlstatus, cookies=cookies_, headers=headers)
    return responstatus.content.decode('utf-8')


def appear(tmp, list) :
    for each in list :
        if each['user'] == tmp['user'] and each['problem'] == tmp['problem'] : return True
    return False

def showList(Ballon_list, vis):
    cnt = 0
    for tmp in Ballon_list:
        flag = True
        for each in vis :
            if tmp['ballon_id'] == each :
                flag = False
        if flag :
            print(tmp)
            cnt = cnt + 1
        if cnt == 10: break

class mainThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()  # 必须调用
        self.work_queue = work_queue
        threading.Thread.__init__(self)

    def run(self):
        # 最新runID
        currentRunID = 0
        # 无重复结果表
        # notRepeatList = []
        cookies = login()
        Ballon_number = 1
        rawlist = []
        while True:
            # 未处理用户列表
            html = getstatus(cookies)
            rawresult = re.findall(pattern, html, re.S)  # list

            for each in reversed(rawresult):
                tmp = {'ballon_id': Ballon_number, 'user': each[2], 'problem': each[4]}
                if eval(each[1]) > currentRunID :
                    if not appear(tmp, rawlist) :
                        rawlist.append(tmp)
                        Ballon_number = Ballon_number + 1
            currentRunID = eval(rawresult[0][1])
            # pp(rawlist)

            while not self.work_queue.empty():
                self.work_queue.get()
            # self.work_queue.put(notRepeatList) # 多线程通信
            self.work_queue.put(rawlist)
            time.sleep(1)


class watchdogThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue

    def run(self):
        Ballon_list = self.work_queue.get()
        alreadySend = []
        vis = []
        showList(Ballon_list, vis)
        while True:
            try:
                index = eval(input())
                if index > 0:
                    cnt = 0
                    for tmp in Ballon_list:
                        if index == tmp['ballon_id']:
                            vis.append(index)
                            alreadySend.append(Ballon_list[cnt])
                            break
                        cnt = cnt + 1
                    # time.sleep(5)
                    Ballon_list = self.work_queue.get()
                    showList(Ballon_list, vis)
                elif index == 0 :
                    Ballon_list = self.work_queue.get()
                    showList(Ballon_list, vis)
                else:
                    for tmp in reversed(alreadySend): print(tmp)
            except:
                Ballon_list = self.work_queue.get()
                showList(Ballon_list,vis)
                print("No!")



def main():
    work_queue = queue.Queue()
    thread1 = mainThread(work_queue=work_queue)
    thread1.daemon = True
    thread1.start()
    time.sleep(3)
    watchdog = watchdogThread(work_queue=work_queue)
    watchdog.daemon = True
    watchdog.start()
    work_queue.join()


if __name__ == '__main__':
    main()