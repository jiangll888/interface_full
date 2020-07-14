import operator as op
import json,re
# from util.telnet import Telnet,Log
from util.linux_conn import do_telnet
from config import settings
from util.read_ini import ReadIni
import os

class Compare:
    def str_cmp(self,expect,result):
        if expect in result:
            return True
        else:
            return False

    def dict_cmp(self,expect,result):
        '''
        字典的完整比较
        :param expect:
        :param result:
        :return:
        '''
        if op.eq(expect,result):
            return True
        else:
            return False

    def dict_partial_cmp2(self,expect,result,cmp_result=True):
        if isinstance(expect,dict):
            for key, value in expect.items():
                if result and not key in result:
                    return False
                else:
                    if result and not value == result[key] and not (isinstance(value,str) and value.isdecimal() and int(value) == result[key]):
                        if isinstance(value, list):
                            for num, item in enumerate(value):
                                cmp_result = self.dict_partial_cmp2(item,result[key][num])
                        elif isinstance(value, dict):
                            cmp_result = self.dict_partial_cmp2(value,result[key])
                        else:
                            return False
        return cmp_result

    def check_for_file(self,expect):
        if len(expect) == 1:
            file_name = expect[0]
        else:
            file_name = expect[1]
        n = do_telnet("ls {}\n".format(file_name))
        # n_count = tn.send('ls -l {} | grep -v "total" | wc -l\n'.format(os.path.dirname(file_name)))
        # count = re.findall(settings.FILE_COUNT_RE, n_count)[-1]
        # count_before = ReadIni().get_value("file_count_before")
        # or int(count) == int(count_before) + 1
        # or int(count) == int(count_before) - 1
        #如果expect只有一个参数说明是希望文件存在的，如果两个参数说明其前面是-，则希望文件不存在
        if len(expect) == 1:
            if "No such file or directory" not in n:
                return True
            else:
                return False
        else:
            if "No such file or directory" in n:
                return True
            else:
                return False



    def compare(self,expect,result=None):
        if not result:
            return self.check_for_file(expect)
        if isinstance(expect,str):
            return self.str_cmp(expect,result)
        elif isinstance(expect,dict):
            return self.dict_partial_cmp2(expect,result)
        else:
            #比如空值比较
            return expect == result

if __name__ == "__main__":
    # a = {'data': 'passWord is:test12345', 'msg': '密码设置成功', 'result': 1, 'success': True}
    # b = {'data': 'passWord is:test12345', 'msg': '密码设置成功', 'result': 1, 'success': True}
    c = Compare()
    # r = c.compare(a,b)
    # print(r)
    d1 = {"code": "BI_SUS-200", "data": {"floorStatus": None, "groupId": "6", "id": "21", "imageUrl": "", "index": 1, "mapUrl": "http://offline-browser-images-test.oss-cn-hangzhou.aliyuncs.com/test/uniubi-bi-group/map/1/2019-10-15T10:21:14.711Z-F1.svg", "name": "1楼"}, "message": "操作成功", "result": 1}
    d2 =  {"code": "BI_SUS-200", "data": {"floorStatus": None, "groupId": 6, "id": 21, "imageUrl": "", "index": 1, "mapUrl": "http://offline-browser-images-test.oss-cn-hangzhou.aliyuncs.com/test/uniubi-bi-group/map/1/2019-10-15T10:21:14.711Z-F1.svg", "name": "1楼"}, "message": "操作成功", "result": 1}
    print(c.compare(d1,d2))