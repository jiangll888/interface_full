import os,sys
sys.path.append(os.path.dirname(os.getcwd()))
import unittest,ddt
from util.opera_db import OperationDB
from base.send_main import SendMain
from config import settings
from BeautifulReport.BeautifulReport import BeautifulReport
import time
from util.log_record import get_logger,get_filename

op_db = OperationDB()
sql = settings.TEST_CASE_SQL
data = op_db.search_all(sql)


@ddt.ddt
class RunCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # os.system(settings.OPEN_TFTP)
        op_db.sql_DML(settings.CLEAR_RESULT_SQL)
        op_db1 = OperationDB(db_name="uniubi_bi_account")
        #清站内信表
        op_db1.sql_DML(settings.CLEAR_SITENOTICE_SQL)
        #清开发者表
        op_db1.sql_DML(settings.CLEAR_DEVELOPER_SQL)
        #清回调表
        op_db1.sql_DML(settings.CLEAR_CALLBACK_SQL)


    @ddt.data(*data)

    @ddt.unpack
    def test01(self,*args,**kwargs):
        self._testMethodDoc = kwargs[settings.CASE_NAME]  #用例注释
        self.is_run = kwargs[settings.IS_RUN]
        if not self.is_run:
            self.skipTest("不执行")         #忽略测试
        get_filename(kwargs[settings.CASE_NAME])
        self.sm = SendMain(kwargs)
        self.res = self.sm.run_main()
        self.assertTrue(self.res)


    def tearDown(self):
        if self.is_run and self.res:
            self.sm.post_act()          #如果执行成功则做数据清理


    @classmethod
    def tearDownClass(cls):
        op_db.close()

if __name__ == "__main__":
    unittest.main()
    # suite = unittest.defaultTestLoader.loadTestsFromTestCase(RunCase)
    # filename = time.strftime("%Y-%m-%d %H-%M-%S")
    # dirname = os.path.join(os.path.dirname(os.getcwd()), "report")
    # isExists = os.path.exists(dirname)
    # if not isExists:
    #     os.makedirs(dirname)
    # BeautifulReport(suite).report(description="接口自动化测试",filename=filename,log_path=dirname)

