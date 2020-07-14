import pymysql,cx_Oracle,sqlite3
from config import settings

def set_db_config(db_type,db_name=None,env="dev"):
    if env == "dev":
        if db_type == "mysql":
            if not db_name:
                db_name = "test"
                host = "127.0.0.1"
                user = "root"
                passwd = "122901"
                db_config = {
                        "host" : host,
                        "port" : 3306,
                        "user" : user,
                        "passwd" : passwd,
                        "db" : db_name,
                        "charset" : 'utf8',
                        "cursorclass" : pymysql.cursors.DictCursor   # 加上cursorclass之后就可以直接把字段名捞出来，和字段值组成键值对的形式
                }
            else:
                host = "rm-bp1t54ibu89062yg2lo.mysql.rds.aliyuncs.com"
                user = "bi"
                passwd = "o7JFQIqhaEo8FGu^"
                db_config = {
                    "host": host,
                    "port": 3306,
                    "user": user,
                    "passwd": passwd,
                    "db": db_name,
                    "charset": 'utf8',
                    "cursorclass": pymysql.cursors.DictCursor  # 加上cursorclass之后就可以直接把字段名捞出来，和字段值组成键值对的形式
                }
        elif db_type == "sqlite":
            if not db_name:
                db_name = "identify_record.db"
            db_config = {
                'database':r'../case/{}'.format(db_name)
            }
        elif db_type == "redis":
            db_config = {
                "host": "172.16.3.210",
                "port":6379,
                "password":"uniubi@123",
                "max_connections":1024
            }
        else:
            if not db_name:
                db_name = "testing"
            tns = cx_Oracle.makedsn("127.0.0.1", 1521, db_name)
            db_config = {
                'user': "root",
                'password': "122901",
                'dsn': tns,
                'nencoding': "utf8"
            }
    else:
            if db_type == "mysql":
                host = "rm-bp1t54ibu89062yg2lo.mysql.rds.aliyuncs.com"
                user = "bi"
                passwd = "o7JFQIqhaEo8FGu^"
                db_config = {
                    "host": host,
                    "port": 3306,
                    "user": user,
                    "passwd": passwd,
                    "db": db_name,
                    "charset": 'utf8',
                    "cursorclass": pymysql.cursors.DictCursor  # 加上cursorclass之后就可以直接把字段名捞出来，和字段值组成键值对的形式
                }
    return db_config
