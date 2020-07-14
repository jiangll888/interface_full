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
SAVE_VALUE = "save_value"
POST_ACTION = "post_action"
EXPECT = "expect"
EXPECT_FOR_DB = "expect_for_db"
RESULT = "result"
TOKEN = "token"
POST_PARAMS = "post_params"


HEADER_URLENCODE = "application/x-www-form-urlencoded"
HEADER_TYPE = "Content-Type"
HEADER_JSON = {"Content-Type":"application/json"}
URL_RE = "^https?://(\d{1,3}.){3}\d{1,3}:\d{1,5}|^https?://.*com/"
FILE_COUNT_RE = "\d+"

DB_TYPE = "mysql"
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWD = "122901"
DB_PORT = 3306
DB_NAME = "test"
TABLE_NAME = "`cases_copy`"

win_ip = "192.168.18.101"
SQLITE_PATH = "E:/工具"
SQLITE_HOST = "192.168.16.240"
SQLITE_USER = "root"
SQLITE_PORT = "23"
SQLITE_PASSWD = "6yhNji9admin"
SQLITE_CMD = "tftp -l {} -r {} -p {}"
# SQLITE_DB_NAME = "person_manager_record.db"
DEV_DB_NAME = ""
OPEN_TFTP = "start {}/tftpd32.exe".format(SQLITE_PATH)

TEST_CASE_SQL = "select * from {};".format(TABLE_NAME)
TABLE_NAME_NOTICE = "site_notice"
CLEAR_RESULT_SQL = "update {} set {}='';".format(TABLE_NAME,RESULT)
CLEAR_SITENOTICE_SQL = "delete from {};".format(TABLE_NAME_NOTICE)
TABLE_NAME_DEVELOPER = "developer"
CLEAR_DEVELOPER_SQL = "delete from {};".format(TABLE_NAME_DEVELOPER)
TABLE_NAME_CALLBACK = "callback_config"
CLEAR_CALLBACK_SQL = "delete from {};".format(TABLE_NAME_CALLBACK)
UPDATE_RESULT_SQL = "update {} set {}=%s where {}=%s;".format(TABLE_NAME,RESULT,CASE_ID)
TABLE_NAME_ACCOUNT = "account"
DELETE_ACCOUNT_SQL = "delete from {} where phone_number=15995807141;".format(TABLE_NAME_ACCOUNT)
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
