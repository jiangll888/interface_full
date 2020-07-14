from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
import time,threading

# 参数times用来模拟网络请求的时间
def get_html(times):
    print(time.strftime("%y-%m-%d %H:%M:%S"))
    print(str(threading.current_thread()) + "  start")
    time.sleep(1)
    print(str(threading.current_thread()) + "  end")

executor = ThreadPoolExecutor(max_workers=3)
urls = [3, 2, 4] # 并不是真的url
all_task = [executor.submit(get_html, (url)) for url in urls]
wait(all_task, return_when=ALL_COMPLETED)
print("main")