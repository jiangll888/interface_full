import operator as op
import json

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

    def dict_partial_cmp(self,expect,result):
        '''
        字典的部分比较
        :param expect:
        :param result:
        :return:
        '''
        for key,value in expect.items():
            if key in result and value == result[key]:
                return True
            else:
                return False

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

    def compare(self,expect,result):
        if isinstance(expect,str):
            return self.str_cmp(expect,result)
        else:
            return self.dict_partial_cmp2(expect,result)

if __name__ == "__main__":
    a = {'data': 'passWord is:test12345', 'msg': '密码设置成功', 'result': 1, 'success': True}
    b = {'data': 'passWord is:test12345', 'msg': '密码设置成功', 'result': 1, 'success': True}
    c = Compare()
    r = c.compare(a,b)
    print(r)
