import requests
import json
from config import settings

class SendRequest:

    def send_get(self,url,data=None,header=None,cookie=None):
        if data:
            data = json.loads(data)
        if cookie and header:
            res = requests.get(url=url,params=data,headers=header,cookies=cookie)
        elif cookie and not header:
            res = requests.get(url=url,params=data,cookies=cookie)
        elif not cookie and header:
            res = requests.get(url=url,params=data,cookies=cookie)
        else:
            res = requests.get(url=url,params=data)
        return res

    def send_post(self,url,data,file=None,param=None,header=None,cookie=None):
        #解决请求中有中文之后截断的问题
        if data:
            data = data.encode(encoding="utf-8")
            if header and settings.HEADER_URLENCODE in header[settings.HEADER_TYPE]:
                # 解决python里的True(用json.loads转换成字典后会变成True)和json字符串里的true不一致会导致失败的问题
                #首先判断里面是否有true，有true才需要替换，否则递归替换耗性能
                if "true" in data.decode("utf-8"):
                    data = self.replace_true(json.loads(data))
                else:
                    data = json.loads(data)
        else:
            data = {}
        if cookie and header:
            res = requests.post(url=url,data=data,json=data,files=file,params=param,headers=header,cookies=cookie)
        elif cookie and not header:
            res = requests.post(url=url,data=data,json=data,files=file,params=param,cookies=cookie)
        elif not cookie and header:
            res = requests.post(url=url,data=data,json=data,files=file,params=param,headers=header)
        else:
            res = requests.post(url=url,data=data,json=data,files=file,params=param)
        return res

    def replace_true(self,data):
        if isinstance(data,dict):
            for key, value in data.items():
                if True == value:
                        data[key] = "true"
                if isinstance(value, list):
                    for num, item in enumerate(value):
                        value[num] = self.replace_true(item)
                if isinstance(value, dict):
                        data[key] = self.replace_true(value)
        return data

    def send_put(self,url,data,header=None,cookie=None):
        # 解决请求中有中文之后截断的问题
        data = data.encode(encoding="utf-8")
        if cookie and header:
            res = requests.put(url=url,data=data,headers=header,cookies=cookie)
        elif cookie and not header:
            res = requests.put(url=url,data=data,cookies=cookie)
        elif not cookie and header:
            res = requests.put(url=url,data=data,headers=header)
        else:
            res = requests.put(url=url,data=data)
        return res

    def send_delete(self,url,data,header=None,cookie=None):
        # 解决请求中有中文之后截断的问题
        data = data.encode(encoding="utf-8")
        if cookie and header:
            res = requests.delete(url=url,data=data,headers=header,cookies=cookie)
        elif cookie and not header:
            res = requests.delete(url=url,data=data,cookies=cookie)
        elif not cookie and header:
            res = requests.delete(url=url,data=data,headers=header)
        else:
            res = requests.delete(url=url,data=data)
        return res

    def send_request(self,method,url,data=None,file=None,param=None,header=None,cookie=None):
        if method.lower() == "get":
            res = self.send_get(url=url,data=data,header=header,cookie=cookie)
        elif method.lower() == "post":
            res = self.send_post(url=url,data=data,file=file,param=param,header=header,cookie=cookie)
        elif method.lower() == "put":
            res = self.send_put(url=url,data=data,header=header,cookie=cookie)
        else:
            res = self.send_delete(url=url,data=data,header=header,cookie=cookie)
        return res

if __name__ == "__main__":
    s = SendRequest()
    d = json.dumps({"a":True})
    print(d)
    print(s.send_post("1",d))



