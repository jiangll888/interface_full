import operator as op
import json
from util.telnet import Telnet,Log
from config import settings

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

    # def dict_partial_cmp(self,expect,result):
    #     '''
    #     字典的部分比较
    #     :param expect:
    #     :param result:
    #     :return:
    #     '''
    #     for key,value in expect.items():
    #         if key in result and value == result[key]:
    #             return True
    #         else:
    #             return False

    def dict_partial_cmp2(self,expect,result,cmp_result=True):
        if isinstance(expect,dict):
            for key, value in expect.items():
                if not key in result:
                    return False
                else:
                    if not value == result[key]:
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
        tn = Telnet(settings.SQLITE_HOST, 23, 1024)
        m = tn.telnet()
        n = tn.send("ls {}\n".format(file_name))
        #如果expect只有一个参数说明是希望文件存在的，如果两个参数说明其前面是-，则希望文件不存在
        if len(expect) == 1:
            if "No such file or directory" in n:
                return False
            else:
                return True
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
    d1 = {'data': {'IDPermission': 2147483647, 'IDnumber': '110101930101123', 'faceAndCardPermission': -1, 'facePermission': 2, 'id': '5382167940', 'idCardPermission': 2, 'idcardNum': '123456789012', 'name': 'liushishi'}, 'msg': '人员信息添加成功', 'result': 1, 'success': True}
    d2 = {'data': {'IDPermission': 2147483647, 'IDnumber': '110101930101123', 'createTime': 1562064355453, 'faceAndCardPermission': -1, 'facePermission': 2, 'id': '5382167940', 'idCardPermission': 2, 'idcardNum': '123456789012', 'name': 'liushishi'}, 'msg': '人员信息添加成功', 'result': 1, 'success': True}

    print(c.compare(d1,d2))