import requests
import json
from config import settings

class OperaToken:
    def __init__(self,filename=None):
        if filename:
            self.filename = filename
        else:
            self.filename = "../config/token.json"

    def write_token(self,res):
        token_value = res.get("data")
        token = {"token":token_value}
        with open(self.filename,"w",encoding='utf-8') as fp:
            json.dump(token,fp)

    def get_token(self):
        try:
            with open(self.filename) as fp:
                res = json.load(fp)
            return res.get(settings.TOKEN)
        except:
            print("打开token文件异常")
            return None