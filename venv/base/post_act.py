from util.opera_db import OperationDB
from config.dataconfig import DataConfig
from config import settings
from base.send_request import SendRequest
from base.opera_cookie import OperaCookie
from jsonpath_rw import parse,jsonpath
import json,re
from util.read_ini import ReadIni
from base.handle_value_list_dict import HandleListOrDict

class PostAct:
    def __init__(self,post_action,post_params,depend_case_id,url):
        self.db = OperationDB()
        self.url = url
        self.post_action = post_action
        self.post_params = post_params
        self.depend_case_id = depend_case_id


    def change_base_url(self,host=None):
        #如果没有传host，则从第一个用例里用正则表达式去匹配host，否则就直接用传入的host
        if not host:
            r = re.search(settings.URL_RE,self.url)
            host = r[0]
        #将host记录到ini文件中，方便后续接口使用
        read_i = ReadIni()
        read_i.write_data("base_url",host,"url")

    def handle_post_action(self):
        if self.post_action:
            for i,post_act in enumerate(self.post_action):
                #参数对应顺序传，否则我不知道你想传给谁
                if "case_id" in post_act:
                    case_id = post_act.split("case_id=")[1]
                    self.send(case_id,self.post_params[i])
                else:
                    func = getattr(self,post_act)
                    if self.post_params and len(self.post_action) == len(self.post_params):
                        func(self.post_params[i])
                    else:
                        func()
        #给依赖的接口所做的操作做清理
        if self.depend_case_id:
            depend_case_id_list = self.depend_case_id.split("|")
            for depend_case_id in depend_case_id_list:
                data = self.get_line_data(depend_case_id)
                self.get_request_data(data)
                #由依赖的接口产生对象去递归调用，这里虽然叫clear什么的，但是此时他是依赖的数据了，并不是清理的
                post_act_obj = PostAct(self.clear_post_action,self.clear_post_params,self.clear_depend_case_id,self.url)
                post_act_obj.handle_post_action()

    def get_line_data(self,case_id):
        '''
        获取数据库里一行数据
        :return:
        '''
        sql = settings.LINE_DATA_SQL
        return case_id and self.db.search_one(sql,case_id)

    def send(self,case_id,post_param):
        sr = SendRequest()
        clear_interface_data = self.get_line_data(case_id)
        self.get_request_data(clear_interface_data)
        if isinstance(post_param,dict):
            post_param = HandleListOrDict().handle_value(post_param)
        #防止递归的时候，依赖的数据的清理动作调用的就是自身，而其实自身已经相当于做了数据清理了
        if self.url != self.clear_url:
            sr.send_request(method=self.clear_method, url=self.clear_url, data=post_param,header=self.clear_header)

    def get_request_data(self,clear_interface_data):
        '''获取当前case的数据'''
        data_config = DataConfig(clear_interface_data)
        self.clear_url = data_config.get_url()
        self.clear_method = data_config.get_method()
        self.clear_header = data_config.get_header()
        self.clear_post_action = data_config.get_post_action()
        self.clear_post_params = data_config.get_post_params()
        self.clear_depend_case_id = data_config.get_depend_case_id()



