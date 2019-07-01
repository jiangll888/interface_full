CASE_ID = "case_id"
CASE_NAME = "case_name"
URL = "url"
METHOD = "method"
HEADER_INFO = "header_info"
IS_WRITE = "is_write"
COOKIE = "cookie"
HEADER = "header"
PARAMS = "params"
PARAM = "param"
DATA = "data"
FILE = "file"
IS_RUN = "is_run"
DEPEND_CASE_ID = "depend_case_id"
DEPEND_REQUEST_FIELD = "depend_request_field"
DEPEND_RESPONSE_FIELD = "depend_response_field"
POST_ACTION = "post_action"
EXPECT = "expect"
EXPECT_FOR_DB = "expect_for_db"
RESULT = "result"
TOKEN = "token"
POST_PARAMS = "post_params"
# BASE_URL = "http://172.16.3.55:8940"
#BASE_URL = "http://study-perf.qa.netease.com"
BASE_URL = "http://192.168.1.68:8090"

HEADER_URLENCODE = "application/x-www-form-urlencoded"
HEADER_TYPE = "Content-Type"
URL_ENCODE = {"Content-Type":"application/x-www-form-urlencoded"}
URL_RE = "^https?://(\d{1,3}.){3}\d{1,3}:\d{1,5}|^https?://.*com/"


DB_TYPE = "mysql"
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWD = "122901"
DB_PORT = 3306
DB_NAME = "test"
TABLE_NAME = "`cases_copy`"

win_ip = "192.168.18.101"
SQLITE_PATH = "E:\工具\资料"
SQLITE_HOST = "192.168.11.88"
SQLITE_USER = "root"
SQLITE_PORT = "23"
SQLITE_PASSWD = ""
SQLITE_CMD = "tftp -l {} -r {} -p {}"

TEST_CASE_SQL = "select * from {};".format(TABLE_NAME)
CLEAR_RESULT_SQL = "update {} set {}='';".format(TABLE_NAME,RESULT)
UPDATE_RESULT_SQL = "update {} set {}=%s where {}=%s;".format(TABLE_NAME,RESULT,CASE_ID)
LINE_DATA_SQL = "select * from {} where {}=%s;".format(TABLE_NAME,CASE_ID)
GET_RESULT_SQL = "select {}  from {};".format(RESULT,TABLE_NAME)

EMAIL_CONTENT = "本次接口自动化执行了{}个测试用例。\n" \
                "其中运行成功{}个，运行失败{}个\n"\
                "测试报告地址:{}\n"\
                "可在数据库中查看运行结果，数据库类型：{}，数据库地址：{}，用户名：{}，密码：{}，"\
                "数据库库名：{}，数据库表名：{}"

EMAIL_SUB = "接口自动化测试报告   {}"
EMAIL_RECEIVER = ["jiangliulin@163.com"]




if __name__ == "__main__":
    change_url("123")
    print(BASE_URL)
