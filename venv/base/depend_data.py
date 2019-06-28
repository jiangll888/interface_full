from util.opera_db import OperationDB
from config.dataconfig import DataConfig
from config import settings
from base.send_request import SendRequest
from base.opera_cookie import OperaCookie
from jsonpath_rw import parse,jsonpath
import json
from base.handle_value_list_dict import HandleListOrDict

class DependData:
    def __init__(self,data):
        self.db = OperationDB()
        self.data = data

    def get_request_data(self):
        '''获取当前case的数据'''
        data_config = DataConfig(self.data)
        params = data_config.get_data()
        return params

    def get_case_id(self):
        '''
        获取依赖的case_id，如果有依赖多个case用 | 去分隔
        :return:
        '''
        data_config = DataConfig(self.data)
        case_ids = data_config.get_depend_case_id()
        case_id_list = case_ids.split("|")
        return case_id_list

    def get_line_data(self,depend_case_id):
        '''
        获取数据库里一行数据
        :return:
        '''
        sql = settings.LINE_DATA_SQL
        return depend_case_id and self.db.search_one(sql,depend_case_id)

    def get_field(self,depend_case_id):
        '''
        获取依赖接口的字段
        :return:
        '''
        self.line_data = self.get_line_data(depend_case_id)
        data_config = DataConfig(self.line_data)
        self.url = data_config.get_url()
        self.method = data_config.get_method()
        self.has_cookie = data_config.has_cookie()
        self.header = data_config.get_header()
        self.request_param = data_config.get_param()
        self.request_data = data_config.get_data()
        self.request_file = data_config.get_file()
        self.depend_case_id = data_config.get_depend_case_id()

    def send_depend_request(self,depend_case_id):
        '''
        发送依赖的接口
        :return:
        '''
        sr = SendRequest()
        oc = OperaCookie()
        self.get_field(depend_case_id)
        if self.depend_case_id:
            data_depend = DependData(self.line_data)
            self.request_data = data_depend.replace_request_data()
        if isinstance(self.request_data,dict):
            self.request_data = HandleListOrDict().handle_value(self.request_data)
        if self.has_cookie:
            cookie = oc.get_cookie()
            res = sr.send_request(self.method, self.url, self.request_data,self.request_file, self.request_param,self.header, cookie)
        else:
            res = sr.send_request(self.method, self.url, self.request_data,self.request_file, self.request_param, self.header)
        return res.json()

    def get_response_field(self):
        '''
        获取返回的依赖字段,如果有依赖多个case用 | 去分隔
        :return:
        '''
        data_config = DataConfig(self.data)
        res_fields = data_config.get_depend_response_field()
        if res_fields:
            res_fields_list = res_fields.split("|")
        return [res_fields.split(";") for res_fields in res_fields_list] # ;用于分隔多个字段

    def get_response_data(self):
        '''
        取出依赖的多个字段
        :return:
        '''
        depend_fields_list = self.get_response_field()
        depend_case_ids = self.get_case_id()
        fields_list = []
        for i, depend_case_id in enumerate(depend_case_ids):
            response_data = self.send_depend_request(depend_case_id)
            fields = []
            if depend_fields_list[i]:
                for depend_field in depend_fields_list[i]:
                    depend_field = parse(depend_field)
                    madle = depend_field.find(response_data)
                    res = [match.value for match in madle][0]
                    fields.append(res)
                fields_list.append(fields)
        return fields_list

    def get_request_field(self):
        '''
            获取返回的请求字段
            :return:
        '''
        data_config = DataConfig(self.data)
        req_fields = data_config.get_depend_request_field()
        if req_fields:
            req_fields_list = req_fields.split("|")
        # req = [json.loads(req_fields) for req_fields in req_fields_list]
        #req = [req_fields for req_fields in req_fields_list]
        return req_fields_list

    def replace_request_data(self):
        response_fields_list = self.get_response_data()
        request_fields_list = self.get_request_field()
        params = self.get_request_data()
        for num,request_fields in enumerate(request_fields_list):
            if request_fields:
                if "{" in request_fields:
                    request_fields = json.loads(request_fields)
                    fields = request_fields["field"].split(";")
                    conn = request_fields["connection"]
                else:
                    fields = request_fields.split(";")
                    conn = None
                for i in range(len(fields)):
                    if conn:
                        params[fields[i]] = conn.join(response_fields_list[num])
                    #params[fields[i]] = response_fields_list[num][i]  #fields是参数的数组，需要与返回参数的数组顺序一致
                    else:
                        field = fields[i].split(".")
                        params = self.replace_json(params,field,response_fields_list[num][i])
        return params

    #替换json中的value,key值传入list
    def replace_json(self,data,key,value):
        if len(key) == 1:
            data[key[0]] = value
        else:
            data[key[0]] = self.replace_json(data[key[0]],key[1:],value)
        return data


if __name__ == "__main__":
    data = {'case_id': 'qingguo_006', 'case_name': '计算运费', 'url': 'http://study-perf.qa.netease.com/common/getTransportFee', 'method': 'get', 'header_info': '{"cookie":"true","header":{"Content-Type": "application/json"}}', 'params': '{"id":1,"addressDetail":""}', 'is_run': 1, 'depend_case_id': 'qingguo_005', 'depend_request_field': '{"field":"addressDetail","connection":"_"}', 'depend_response_field': 'result.list.[0].province;result.list.[0].city;result.list.[0].area', 'expect': '"message":"success"', 'result': None}
    d = DependData(data)
    d.get_field()
    print(d.url)
    res = d.handle_depend_data()
    print(type(res))

