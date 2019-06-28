import unittest, ddt
from util.opera_db import OperationDB
from base.send_main import SendMain
from config import settings
from BeautifulReport.BeautifulReport import BeautifulReport
import time

op_db = OperationDB()
sql = settings.TEST_CASE_SQL
data = op_db.search_all(sql)
count = 0

rn =0
@ddt.ddt
class RunCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        op_db.sql_DML(settings.CLEAR_RESULT_SQL)

    def setUp(self):
        print(data[count][settings.IS_RUN])


    @ddt.data(*data)
    @ddt.unpack
    #@unittest.skipIf(not data[count][settings.IS_RUN], "test")
    def test01(self, *args, **kwargs):
        '''测试注释'''
        if kwargs[settings.IS_RUN] == 0:
            self.skipTest("TEST")
        print("test01")
        # print(data[count][settings.IS_RUN],type(data[count][settings.IS_RUN]))
        # if data[count][settings.IS_RUN] == 0:
        #     print("yes")

    def tearDown(self):
        print(self.__dict__["_testMethodDoc"])

    @classmethod
    def tearDownClass(cls):
        op_db.close()


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RunCase)
    filename = time.strftime("%Y-%m-%d %H-%M-%S")
    BeautifulReport(suite).report(description="接口自动化测试",filename=filename,log_path="../report")

