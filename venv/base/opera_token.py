import requests
import json
from config import settings
from util.log_record import get_logger

class OperaToken:
    def __init__(self,filename=None):
        self.logger = get_logger()
        if filename:
            self.filename = filename
        else:
            self.filename = "../config/token.json"

    def write_token(self,res):
        token_value = res.get("data").get("token")
        token = {"token":token_value}
        with open(self.filename,"w",encoding='utf-8') as fp:
            json.dump(token,fp)
            self.logger.info("写入token，token为  "
                             "{}".format(token_value))


    def get_token(self):
        try:
            with open(self.filename) as fp:
                res = json.load(fp)
            return res.get(settings.TOKEN)
        except:
            print("打开token文件异常")
            self.logger.info("打开token文件异常，token文件为".format(self.filename))
            return None