from util import opera_db
from config import settings
from util.opera_db import OperationDB
import json
import random
from util.read_ini import ReadIni
from base.opera_token import OperaToken
from util.linux_conn import do_telnet

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
        return url

    def get_method(self):
        return self.db_data and self.db_data[settings.METHOD]

    def get_header_info(self):
        if self.db_data and not self.db_data[settings.HEADER_INFO]:
            return settings.URL_ENCODE
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
            #如果有传"header"的key在里面，则取出来
            elif settings.HEADER in header_info:
                header = header_info[settings.HEADER]
            #如果里面有token，则用文件里已经取到的token去替换
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

    def replace_randnum(self,data):
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

    def get_expext(self):
        return self.db_data and self.db_data[settings.EXPECT]

    def get_expect_for_db(self):
        expect = self.get_expext()
        if expect and "{" in expect:
            if "##" in expect:
                #如果里面有需要替换的动态变量，才去走替换函数，提高性能，否则每次不管有没有要替换的变量，都要去递归判断每个变量是否需要替换，接口比较多的话会耗时多
                expect = self.replace_randnum(json.loads(expect))
            else:
                expect = json.loads(expect)
            if settings.EXPECT_SQL in expect:
                sql = expect[settings.EXPECT_SQL]
                #从设备上把db文件拷贝下来，传过来的需要告知是查询哪张表，如果不传给个默认
                do_telnet(db_name)
                #打开数据库连接
                op_db = OperationDB("sqlite",db_name)
                expect = op_db.search_one(sql)
        return expect

    def get_result(self):
        return self.db_data and self.db_data[settings.RESULT]

    def write_result(self,sql,param):
        self.op_db.sql_DML(sql,param)

if __name__ == "__main__":
    db = OperationDB()
    sql = "select * from cases_copy where case_id=%s"
    pa = ("5C_001",)
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
    # print(d.get_url())
    # print(d.rand_str(),type(d.rand_str()))
    # data1 = {"pass":"test12345","person":{"id":"##id","idcardNum":123,"name":"Neo","IDPermission":2}}
    # print(d.replace_randnum(data1))


