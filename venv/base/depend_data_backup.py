from util.opera_db import OperationDB
from config.dataconfig import DataConfig
from config import settings
from base.send_request import SendRequest
from base.opera_cookie import OperaCookie
from jsonpath_rw import parse,jsonpath
import json

class DependData:
    def __init__(self,data):
        self.db = OperationDB()
        self.data = data

    def get_request_data(self):
        data_config = DataConfig(self.data)
        params = data_config.get_data()
        return params

    def get_case_id(self):
        '''
        获取依赖的case_id
        :return:
        '''
        data_config = DataConfig(self.data)
        return data_config.get_depend_case_id()

    def get_line_data(self):
        '''
        获取数据库里一行数据
        :return:
        '''
        depend_case_id = self.get_case_id()
        sql = settings.LINE_DATA_SQL
        return depend_case_id and self.db.search_one(sql,depend_case_id)

    def get_field(self):
        '''
        获取依赖接口的字段
        :return:
        '''
        line_data = self.get_line_data()
        data_config = DataConfig(line_data)
        self.url = data_config.get_url()
        self.method = data_config.get_method()
        self.has_cookie = data_config.has_cookie()
        self.header = data_config.get_header()
        self.request_data = data_config.get_params()

    def send_depend_request(self):
        '''
        发送依赖的接口
        :return:
        '''
        sr = SendRequest()
        oc = OperaCookie()
        self.get_field()
        if self.has_cookie:
            cookie = oc.get_cookie()
            res = sr.send_request(self.method, self.url, self.request_data, self.header, cookie)
        else:
            res = sr.send_request(self.method, self.url, self.request_data, self.header)
        return res.json()

    def get_response_field(self):
        '''
        获取返回的依赖字段
        :return:
        '''
        data_config = DataConfig(self.data)
        res_fields = data_config.get_depend_response_field()
        return res_fields and res_fields.split(";")

    def get_response_data(self):
        '''
        取出依赖的多个字段
        :return:
        '''
        response_data= self.send_depend_request()
        depend_fields = self.get_response_field()
        fields = []
        if depend_fields:
            for depend_field in depend_fields:
                depend_field = parse(depend_field)
                madle = depend_field.find(response_data)
                res = [match.value for match in madle][0]
                fields.append(res)
        return fields

    def get_request_field(self):
        '''
            获取返回的请求字段
            :return:
        '''
        data_config = DataConfig(self.data)
        req_fields = data_config.get_depend_request_field()
        return json.loads(req_fields)

    def replace_request_data(self):
        response_fields = self.get_response_data()
        request_fields = self.get_request_field()
        params = self.get_request_data()
        if request_fields:
            fields = request_fields["field"]
            conn = request_fields["connection"]
            if conn:
                params[fields] = conn.join(response_fields)
            else:
                for i in range(len(fields)):
                    params[fields[i]] = response_fields[i]
        return params

    def handle_depend_data(self):
        if self.get_case_id():
            params = self.replace_request_data()
            return params and json.dumps(params)
        else:
            params = self.get_request_data()
            return params and json.dumps(params)

if __name__ == "__main__":
    data = {'case_id': 'qingguo_006', 'case_name': '计算运费', 'url': 'http://study-perf.qa.netease.com/common/getTransportFee', 'method': 'get', 'header_info': '{"cookie":"true","header":{"Content-Type": "application/json"}}', 'params': '{"id":1,"addressDetail":""}', 'is_run': 1, 'depend_case_id': 'qingguo_005', 'depend_request_field': '{"field":"addressDetail","connection":"_"}', 'depend_response_field': 'result.list.[0].province;result.list.[0].city;result.list.[0].area', 'expect': '"message":"success"', 'result': None}
    d = DependData(data)
    d.get_field()
    print(d.url)
    res = d.handle_depend_data()
    print(type(res))

