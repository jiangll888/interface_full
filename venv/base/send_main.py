from base.send_request import SendRequest
from config.dataconfig import DataConfig
from base.opera_cookie import OperaCookie
from base.opera_token import OperaToken
from base.depend_data import DependData
from util.opera_db import OperationDB
from util.compare import Compare
import json
import threading
from config import settings
from base.handle_value_list_dict import HandleListOrDict
from util.read_ini import ReadIni
import re
from base.post_act import PostAct

class SendMain:
    _instance_lock = threading.Lock()

    def __init__(self,data):
        self.data = data
        self.get_field()
        self.retry_count = 0
        self.cmp = Compare()
        self.ot = OperaToken()
        self.sr = SendRequest()
        #self.oc = OperaCookie()

    def __new__(cls, *args, **kwargs):
        '''
        实现单例模式
        :param args:
        :param kwargs:
        :return:
        '''
        if not hasattr(cls,"_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def get_field(self):
        dc = DataConfig(self.data)
        self.case_id = dc.get_case_id()
        self.url = dc.get_url()
        self.method = dc.get_method()
        self.is_write = dc.is_write()
        self.is_run = dc.get_is_run()
        self.has_cookie = dc.has_cookie()
        self.header = dc.get_header()
        self.request_param = dc.get_param()
        self.request_data = dc.get_data()
        self.request_file = dc.get_file()
        self.depend_case_id = dc.get_depend_case_id()
        self.expect = dc.get_expect_for_db()
        self.post_action = dc.get_post_action()
        self.post_params = dc.get_post_params()

    def run_main_iter(self):
        dd = DependData(self.data)
        # if self.is_run:
        if self.depend_case_id:
            self.request_data = dd.replace_request_data()
        if isinstance(self.request_data,dict):
            self.request_data = HandleListOrDict().handle_value(self.request_data)
        #if self.has_cookie:
            #cookie = self.oc.get_cookie()
        #     res = self.sr.send_request(self.method,self.url,self.request_data,self.request_file,self.request_param,self.header,cookie)
        # else:
        res = self.sr.send_request(self.method, self.url, self.request_data,self.request_file,self.request_param, self.header)
        return res

    def run_main(self):
        while self.is_run:
            res = self.run_main_iter()
            if self.retry_count < 2 and res.status_code >= 500:
                # 如果在重试次数范围内，返回的是服务器错误，则继续重试
                self.retry_count += 1
                print("重试第{}次".format(self.retry_count))
                # self.run_main_iter()
            elif self.retry_count >= 2 and res.status_code >= 500:
                #如果重试到最后，返回的还是服务器错误，则认为其失败，终止循环
                r = False
                break
            else:
                try:
                    print(res.json())
                    r = self.cmp.compare(self.expect, res.json())
                except Exception as e:
                    print("发生了未知错误: {}".format(e))
                    r = False
                break
        if self.is_run:
            if res and self.is_write:
            # oc.write_cookie(res)
                self.ot.write_token(res.json())
            self.write_res(r)
            return r

    def write_res(self,res):
        dc = DataConfig(self.data)
        sql = settings.UPDATE_RESULT_SQL
        if res:
            para = ("pass", self.case_id)
        else:
            para = ("fail", self.case_id)
        dc.write_result(sql,para)

    def post_act(self):
        '''
        数据清理操作
        :return:
        '''
        if self.post_action or self.depend_case_id:
            post_act_obj = PostAct(self.post_action,self.post_params,self.depend_case_id,self.url)
            post_act_obj.handle_post_action()
        # if self.post_action:
        #     op_db = OperationDB()
        #     op_db.sql_DML(self.post_action)        #直接用sql语句做数据清理



if __name__ == "__main__":
    db = OperationDB()
    sql = "select * from cases where case_id=%s"
    pa = ("qingguo_001",)
    data = db.search_one(sql, pa)
    s = SendMain(data)
    r = s.run_main()
    # s.change_base_url()
    print(r)
