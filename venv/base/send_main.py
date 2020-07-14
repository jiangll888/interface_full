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
from base.handle_save_value import HandleSaveValue
from util.log_record import get_logger
import os

class SendMain:
    _instance_lock = threading.Lock()

    def __init__(self,data):
        self.data = data
        self.get_field()
        self.retry_count = 0
        self.cmp = Compare()
        self.ot = OperaToken()
        self.sr = SendRequest()
        self.logger = get_logger()
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
        self.save_value = dc.get_save_value()
        #记录跑之前目录下文件数量
        # dc.get_expect_for_other_before()

    def run_main_iter(self):
        dd = DependData(self.data)
        # if self.is_run:
        if self.depend_case_id:
            self.request_data = dd.replace_request_data()
        if isinstance(self.request_data,dict) or isinstance(self.request_data,list):
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
                self.logger.warn("重试第{}次".format(self.retry_count))
            elif self.retry_count >= 2 and res.status_code >= 500:
                #如果重试到最后，返回的还是服务器错误，则认为其失败，终止循环
                r = False
                break
            else:
                # try:
                    print("返回结果: " + str(res.json()))
                    self.logger.info("返回结果:{}".format(res.json()))
                    if self.save_value:
                        HandleSaveValue().save_response_data(res.json(),self.save_value)
                    dc = DataConfig(self.data)
                    r1 = r2 = r3 = True
                    self.expect_for_db = dc.get_expect_for_db()
                    self.expect_for_other = dc.get_expect_for_other()
                    if self.expect_for_db:
                        # 如果只传了sql语句，说明想与返回结果对比
                        if len(self.expect_for_db) == 1:
                            r1 = self.cmp.compare(self.expect_for_db[0], res.json())
                            self.logger.info("返回结果与数据库查询结果进行对比，对比结果是{}".format(r1))
                        else:
                            # 如果传了两个参数，则前面是sql语句，后面是希望sql查询出的结果
                            r1 = self.cmp.compare(self.expect_for_db[0], self.expect_for_db[1])
                            self.logger.info("数据库预期结果与数据库查询结果进行对比，对比结果是{}".format(r1))
                    # 如果传了expect_for_other则会做与接口的返回结果对比
                    if self.expect_for_other:
                        # 与接口返回结果对比
                        r2 = self.cmp.compare(self.expect_for_other[0], res.json())
                        self.logger.info("预期接口返回结果与实际接口返回结果进行对比，对比结果是{}".format(r2))
                        if len(self.expect_for_other) == 2:
                            # 如果传了第二个参数则要判断文件是否存在
                            r3 = self.cmp.compare(self.expect_for_other[1])
                            self.logger.info("判断文件是否存在，对比结果是{}".format(r3))
                    r = r1 and r2 and r3
                    break
                # except Exception as e:
                #     print("发生了未知错误: {}".format(e))
                #     self.logger.error("发生了未知错误: {}".format(e))
                #     r = False
                #     break
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
            self.logger.info("将结果写入数据库，结果为pass")
        else:
            para = ("fail", self.case_id)
            self.logger.error("将结果写入数据库，结果为fail，case_id为{}".format(self.case_id))
        dc.write_result(sql,para)

    def post_act(self):
        '''
        数据清理操作
        :return:
        '''
        dc = DataConfig(self.data)
        self.post_action = dc.get_post_action()
        self.post_params = dc.get_post_params()
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
