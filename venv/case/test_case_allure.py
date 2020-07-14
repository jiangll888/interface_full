import os,sys
sys.path.append(os.path.dirname(os.getcwd()))
import unittest,ddt
from util.opera_db import OperationDB
from base.send_main import SendMain
from config import settings
from BeautifulReport.BeautifulReport import BeautifulReport
import time
import pytest,allure
from util.read_ini import ReadIni

op_db = OperationDB()
sql = settings.TEST_CASE_SQL
data = op_db.search_all(sql)
read_i = ReadIni()


class Test01:
    def setup_class(self):
        os.system(settings.OPEN_TFTP)
        op_db.sql_DML(settings.CLEAR_RESULT_SQL)

    def setup_method(self):
        pass

    @allure.title("接口自动化用例")
    @allure.feature("test case module")
    @allure.story("test case story")
    @allure.severity("normal")
    @allure.title("{param1}")
    @pytest.mark.parametrize('param1,param2',zip(list(map(lambda x:x[settings.CASE_NAME],data)),data))
    @pytest.mark.test
    def test01(self,param1,param2):
        self._testMethodDoc = param2[settings.CASE_NAME]  #用例注释
        self.is_run = param2[settings.IS_RUN]
        if not self.is_run:
            pytest.skip("不执行")         #忽略测试
        self.sm = SendMain(param2)
        self.res = self.sm.run_main()
        assert self.res

    def teardown_method(self):
        if self.is_run and self.res:
            self.sm.post_act()          #如果执行成功则做数据清理

    def teardown_class(self):
        op_db.close()


if __name__ == "__main__":
    pass


