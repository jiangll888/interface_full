import  threading,multiprocessing
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import random,math

ticketIds = []
t1111 = []
t111 = []
t11_11 = []
t1_11 = []
t100_ticket = []
t1_11_ticket = []
d = {"T_1111_YUAN":0,"T_111_YUAN":0,"T_11_POINT_11_YUAN":0,"T_1_POINT_11_YUAN":0,"T_100_TICKET":0,"T_1_POINT_11_TICKET":0}
count = 0
executor = ThreadPoolExecutor()

def run(click):
    global d
    global count
    for j in range(5):
        # lock.acquire()
        count += 1
        # lock.release()
        res = requests.get(url="http://yintai.heydayscape.com:8010/wechat/virtual/user")
        print(res.json())
        code = res.json().get("data").get("code")
        openId = res.json().get("data").get("openId")
        url1 = "http://yintai.heydayscape.com:8010/ticket/draw/{}".format(click)
        header = {"code":code,"openId":openId}
        res1 = requests.get(url=url1,headers=header)
        print(res1.json())
        data = res1.json().get("data")
        if data:
            ticketId0 = data[0].get("ticketId")
            type0 = data[0].get("type")
            ticketIds.append(ticketId0)
            d[type0] = d[type0] + 1
            if len(data) == 2:
                ticketId1 = data[1].get("ticketId")
                type1 = data[1].get("type")
                ticketIds.append(ticketId1)
                d[type1] = d[type1] + 1


def noRepeat():
    ticketIds1= ticketIds
    r = [t for t in ticketIds if t in ticketIds1]
    print(r)

def test():
    # global d
    # global count
    # for i in range(3):
        # d[type0] = d[type0] + 1
        # count += 1
        # print(threading.enumerate())
        # print(threading.activeCount())
        # print(threading.current_thread().isAlive())
    # print(threading.current_thread().name + "开始执行")
    # time.sleep(3)
    # print(threading.current_thread().name + "执行结束")
    # for i in range(2):
    #     executor.submit(do_update)
    # return 'ok'
    for i in range(300):
        if i >=0 and i<=9:
            phone_last = "00" + str(i)
        elif i>=10 and i<=99:
            phone_last = "0" + str(i)
        else:
            phone_last = str(i)
        phone = "15859523" + phone_last
        print(phone)

def test1():
    global count
    for i in range(3):
        count += 1

def do_update():
    time.sleep(1)
    print('start update cache')
    time.sleep(1)
    print("end")


if __name__ == "__main__":
    # lock = threading.Lock()
    # for i in range(10):
    #     t = threading.Thread(target=run,args=(i+1,))
    #     t.start()
    #     t.join()
    # print(d)
    # with open("../config/token.json", "w") as fp:
    #     json.dump(d, fp)
    # pool = []
    # for i in range(2):
    #     t = threading.Thread(target=test,args=(i+1,))
    #     pool.append(t)
    # for n in pool:
    #     n.start()
    #     n.join()
    # print(threading.current_thread().name)
    # test()
    # print(threading.current_thread().name)
    # print(count)
    # pool = multiprocessing.Pool(10)
    # for i in range(2):
    #     pool.apply_async(func=run, args=(i+1,))
    # pool.close()
    # pool.join()
    # noRepeat()
    # print(math.floor(random.random()*10)+1)
    executor = ThreadPoolExecutor(max_workers=200)
    all_task = [executor.submit(run,(i+1)) for i in range(10)]
    wait(all_task, return_when=ALL_COMPLETED)
    print(count)