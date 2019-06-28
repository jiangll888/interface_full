import requests
import json

class OperaCookie:
    def __init__(self,filename=None):
        if filename:
            self.filename = filename
        else:
            self.filename = "../config/cookie.json"

    def write_cookie(self,res):
        cookie = res.cookies
        cookie = requests.utils.dict_from_cookiejar(cookie)
        with open(self.filename,"w",encoding='utf-8') as fp:
            json.dump(cookie,fp)

    def get_cookie(self):
        try:
            with open(self.filename) as fp:
                res = json.load(fp)
            return res
        except:
            print("打开cookie文件异常")
            return None