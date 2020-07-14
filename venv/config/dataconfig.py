from util import opera_db
from config import settings
from util.opera_db import OperationDB
import json,time,os
import random
from util.read_ini import ReadIni
from base.opera_token import OperaToken
from util.linux_conn import do_telnet
from util.telnet import Telnet
import re
import hashlib
from util.handle_md5 import get_des_psswd

class DataConfig:

    def __init__(self,data):
        self.db_data = data
        self.op_db = OperationDB()
        self.read_i = ReadIni()

    def get_case_id(self):
        return self.db_data and self.db_data[settings.CASE_ID]

    def get_case_name(self):
        return self.db_data and self.db_data[settings.CASE_NAME]

    def get_url(self):
        if self.db_data:
            url =  self.db_data[settings.URL]
            base_url = self.read_i.get_value("base_url","url")
            #如果用例里没写base_url才加上
            if base_url not in url:
                url = base_url + url
            if "##" in url:
                url = self.replace_randnum_for_str(url)
            print("请求url： " + url)
        return url

    def get_method(self):
        return self.db_data and self.db_data[settings.METHOD]

    def get_header_info(self):
        if self.db_data and not self.db_data[settings.HEADER_INFO]:
            return settings.HEADER_JSON
        return self.db_data and self.db_data[settings.HEADER_INFO] and json.loads(self.db_data[settings.HEADER_INFO])

    def is_write(self):
        header_info = self.get_header_info()
        if header_info and settings.IS_WRITE in header_info:
            return header_info[settings.IS_WRITE]
        else:
            return None

    def has_cookie(self):
        header_info = self.get_header_info()
        if header_info and settings.COOKIE in header_info:
            return header_info[settings.COOKIE]
        else:
            return None

    def get_header(self):
        header_info = self.get_header_info()
        #header如果没有"header"的key在里面，则当他就是header
        if header_info:
            if not (settings.HEADER in header_info or
                settings.IS_WRITE in header_info or
                settings.COOKIE in header_info):
                header = header_info
                # 如果里面有token，则用文件里已经取到的token去替换
                if settings.TOKEN in header:
                    ot = OperaToken()
                    header[settings.TOKEN] = ot.get_token()
                return header
            #如果有传"header"的key在里面，则取出来
            if settings.HEADER in header_info:
                header = header_info[settings.HEADER]
                # 如果里面有token，则用文件里已经取到的token去替换
                if settings.TOKEN in header:
                    ot = OperaToken()
                    header[settings.TOKEN] = ot.get_token()
                return header
        else:
            return None

    def get_params(self):
        return self.db_data and self.db_data[settings.PARAMS]  and json.loads(self.db_data[settings.PARAMS])

    def get_param(self):
        params = self.get_params()
        if params and settings.PARAM in params:
            return json.dumps(params[settings.PARAM])
        else:
            return None

    def get_data(self):
        params = self.get_params()
        if params:
            if not (settings.PARAM in params or
                    settings.FILE in params or
                    settings.DATA in params):
                data = params
            elif settings.DATA in params:
                data =  params[settings.DATA]
            # 如果里面有需要替换的动态变量，才去走替换函数，提高性能，否则每次不管有没有要替换的变量，都要去递归判断每个变量是否需要替换，接口比较多的话会耗时多
            if "func" in json.dumps(data):
                data = self.handle_value(data)
            if "##" in json.dumps(data):
                data = self.replace_randnum(data)
            print("请求数据: " + str(data))
            return data
        else:
            return None


    def handle_value(self,data):
        if isinstance(data,dict):         #{"pass":"test12345","person":{"id":{"func":"rand_num"},"idcardNum":{"func":"rand_str"},"name":"Neo","IDPermission":2}}
            for key, value in data.items():
                if isinstance(value, list):
                    for num, item in enumerate(value):
                        value[num] = self.handle_value(item)
                if isinstance(value,dict):
                    if "func" in value:
                        func = value["func"]
                        func = getattr(self, func)
                        data[key] = func()
                        self.read_i.write_data(key, str(data[key]))
                    else:
                        data[key] = self.handle_value(value)
        return data

    #获取当前时间戳
    def get_timestamp(self):
        self.current_time = str(int(round(time.time(), 3) * 1000))
        return self.current_time

    #根据时间戳、accessKey、accessSerect经由MD5 32位生成的密钥签名
    def get_sign(self):
        accessKey = self.read_i.get_value("data.accessKey")
        accessSerect = self.read_i.get_value("data.accessSecret")
        return get_des_psswd(self.current_time,accessKey,accessSerect)

    def replace_randnum(self,data):
        #如果一开始就是个list
        if isinstance(data,list):
            for n, i in enumerate(data):
                data[n] = self.replace_randnum(i)
        if isinstance(data,dict):         #{"pass":"test12345","person":{"id":"##id","idcardNum":123,"name":"Neo","IDPermission":2}}
            for key, value in data.items():
                if isinstance(value,str):
                    #如果里面含有##则替换动态参数，从global_var.ini里查出来
                    if "##" in value:
                        value = value.split("##")[1]
                        data[key] = self.read_i.get_value(value)
                if isinstance(value, list):
                    for num, item in enumerate(value):
                        value[num] = self.replace_randnum(item)
                if isinstance(value, dict):
                        data[key] = self.replace_randnum(value)
        return data

    def replace_randnum_for_str(self, data):
        if isinstance(data,str):  # select col_1,col_2 from person_table where col_1="##id";
            # 如果里面含有##则替换动态参数，从global_var.ini里查出来
            p = "(?<=##).+[^_##|\"]"
            if "##" in data:
                # value = data.split("##")[1].split("\"")[0]
                value_list = re.findall(p,data)
                for value in value_list:
                    data = data.replace("##{}".format(value),self.read_i.get_value(value))
        return data

    def rand_num(self):
        return random.randint(10000001,100000000)

    def rand_str(self):
        return ''.join(random.sample(['0','1','2','3','4','5','6','7','8','9'],10))

    def get_file(self):
        params = self.get_params()
        if params and settings.FILE in params:
            # return json.dumps(params[settings.FILE])
            params[settings.FILE][settings.FILE] = eval(params[settings.FILE][settings.FILE])
            return params[settings.FILE]
        else:
            return None

    def get_is_run(self):
        return self.db_data and self.db_data[settings.IS_RUN]

    def get_depend_case_id(self):
        return self.db_data and self.db_data[settings.DEPEND_CASE_ID]

    def get_depend_request_field(self):
        return self.db_data and self.db_data[settings.DEPEND_REQUEST_FIELD]

    def get_depend_response_field(self):
        return self.db_data and self.db_data[settings.DEPEND_RESPONSE_FIELD]

    def get_save_value(self):
        return self.db_data and self.db_data[settings.SAVE_VALUE]

    def get_post_action(self):
        if self.db_data and settings.POST_ACTION in self.db_data:
            post_action = self.db_data[settings.POST_ACTION]
            if post_action:
                post_action_list = post_action.split("|")
                return post_action_list
        return None

    def get_post_params(self):
        if self.db_data and settings.POST_PARAMS in self.db_data:
            post_params = self.db_data[settings.POST_PARAMS]
            if post_params:
                post_params_list = post_params.split("|")
                for i,post_params in enumerate(post_params_list):
                    if "{" in post_params:
                        if "##" in post_params:
                            post_params_list[i] = self.replace_randnum(json.loads(post_params))
                        else:
                            post_params_list[i] = json.loads(post_params)
                return post_params_list
        return None

    def replace_true(self,data):
        if isinstance(data,dict):
            for key, value in data.items():
                if "true" == value:
                        data[key] = True
                if isinstance(value, list):
                    for num, item in enumerate(value):
                        value[num] = self.replace_true(item)
                if isinstance(value, dict):
                        data[key] = self.replace_true(value)
        return data

    def get_expect_for_db(self):
        if self.db_data and self.db_data[settings.EXPECT_FOR_DB]:
            expect = self.db_data[settings.EXPECT_FOR_DB]
            # 如果有多个参数，比如前面是sql语句，后面是期望这个sql语句返回的结果
            expect_list = expect.split("|")
            expect_list[0] = self.replace_randnum_for_str(expect_list[0])
            db_and_sql = expect_list[0].split(">")
            if len(db_and_sql) == 2:
                db_name = db_and_sql[0]
                sql = db_and_sql[1]
            else:
                db_name = settings.DEV_DB_NAME
                sql = db_and_sql[0]
            # 从设备上把db文件拷贝下来，传过来的需要告知是查询哪张表，如果不传给个默认
            # print(settings.SQLITE_CMD.format(db_name,db_name,settings.win_ip))
            # do_telnet(settings.SQLITE_CMD.format(db_name,db_name,settings.win_ip))
            # 打开数据库连接
            # op_db = OperationDB("sqlite", db_name)
            op_db = OperationDB(settings.DB_TYPE, db_name)
            expect_list[0] = op_db.search_one(sql)
            if len(expect_list) == 2:
                # 如果查不到的就预期空值，比如删除了的
                if expect_list[1] == "None":
                    expect_list[1] = eval(expect_list[1])
                elif "{" in expect_list[1]:
                    if "##" in expect_list[1]:
                        # 如果里面有需要替换的动态变量，才去走替换函数，提高性能，否则每次不管有没有要替换的变量，都要去递归判断每个变量是否需要替换，接口比较多的话会耗时多
                        expect_list[1] = self.replace_randnum(json.loads(expect_list[1]))
                    else:
                        expect_list[1] = json.loads(expect_list[1])
                    if "true" in json.dumps(expect_list[1]):
                        expect_list[1] = self.replace_true(expect_list[1])
            return expect_list

    # def get_expect_for_other_before(self):
    #     if self.db_data and self.db_data[settings.EXPECT]:
    #         expect = self.db_data[settings.EXPECT]
    #         # 如果有多个参数，比如前面是预期的接口返回结果，后面是文件是否存在（希望文件不存在的可以标注not=文件名）
    #         expect_list = expect.split("|")
    #         if len(expect_list) == 2:
    #             # 如果不希望文件存在呢，则在文件前面加-
    #             expect = expect_list[1].split("-")
    #             if len(expect) == 1:
    #                 file_name = expect[0]
    #             else:
    #                 file_name = expect[1]
    #            # n = do_telnet("ls {}\n".format(file_name))
    #             count = re.findall(settings.FILE_COUNT_RE,n)[-1]
    #             self.read_i.write_data("file_count_before",count)

    def get_expect_for_other(self):
        if self.db_data and self.db_data[settings.EXPECT]:
            expect = self.db_data[settings.EXPECT]
            # 如果有多个参数，比如前面是预期的接口返回结果，后面是文件是否存在（希望文件不存在的可以标注-）
            expect_list = expect.split("|")
            if "{" in expect_list[0]:
                if "##" in expect_list[0]:
                    # 如果里面有需要替换的动态变量，才去走替换函数，提高性能，否则每次不管有没有要替换的变量，都要去递归判断每个变量是否需要替换，接口比较多的话会耗时多
                    expect_list[0] = self.replace_randnum(json.loads(expect_list[0]))
                else:
                    expect_list[0] = json.loads(expect_list[0])
                if "true" in json.dumps(expect_list[0]):
                    expect_list[0] = self.replace_true(expect_list[0])
            if len(expect_list) == 2:
                expect_list[1] = self.replace_randnum_for_str(expect_list[1])
                # 如果不希望文件存在呢，则在文件前面加-
                expect_list[1] = expect_list[1].split("-")
            print("预期结果： " + str(expect_list))
            return expect_list



    def get_result(self):
        return self.db_data and self.db_data[settings.RESULT]

    def write_result(self,sql,param):
        self.op_db.sql_DML(sql,param)

if __name__ == "__main__":
    db = OperationDB()
    sql = "select * from cases_copy where case_id=%s"
    pa = ("5C_003",)
    data = db.search_one(sql,pa)
    print(data)
    # print(data[settings.PARAMS],type(data[settings.PARAMS]))
    d = DataConfig(data)
    print(1111111111111)
    #print(d.get_expect_for_db())
    # print(d.get_params())
    # print(d.get_file(),type(d.get_file()))
    # print(d.get_header())
    #d.read_i.write_data("1","2")
    r = d.get_data()
    print(r,type(r))
    res1 = d.replace_randnum_for_str('select col_1,col_2 from person_table where col_1="##id";')
    print(res1)
    print(d.get_expect_for_other())
    print(d.get_sign())
    # print(d.get_url())
    # print(d.rand_str(),type(d.rand_str()))
    # data1 = {"pass":"test12345","person":{"id":"##id","idcardNum":123,"name":"Neo","IDPermission":2}}
    # print(d.replace_randnum(data1))


