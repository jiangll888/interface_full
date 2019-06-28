import pymysql,cx_Oracle,sqlite3
from config import settings

def set_db_config(db_type,db_name=None,env="dev"):
    if env == "dev":
        if db_type == "mysql":
            if not db_name:
                db_name_local = "test"
            db_config = {
                    "host" : "127.0.0.1",
                    "port" : 3306,
                    "user" : "root",
                    "passwd" : "122901",
                    "db" : db_name_local,
                    "charset" : 'utf8',
                    "cursorclass" : pymysql.cursors.DictCursor   # 加上cursorclass之后就可以直接把字段名捞出来，和字段值组成键值对的形式
            }
        elif db_type == "sqlite":
            if not db_name:
                db_name_local = "identify_record.db"
            db_config = {
                'database':r'{}\{}'.format(settings.SQLITE_PATH,db_name_local)
            }
        else:
            if not db_name:
                db_name_local = "testing"
            tns = cx_Oracle.makedsn("127.0.0.1", 1521, db_name_local)
            db_config = {
                'user': "root",
                'password': "122901",
                'dsn': tns,
                'nencoding': "utf8"
            }
    return db_config
