#coding:utf-8
import cx_Oracle
import pymysql,sqlite3
from DBUtils.PooledDB import PooledDB
from config import  settings
from config.set_db_config import set_db_config
import threading
import redis

class OperationDB:
    _instance_lock = threading.Lock()

    def __init__(self,db_type=settings.DB_TYPE,db_name=None,env="dev"):
        self.db_type = db_type
        # if db_type == 'oracle':
        #     tns = cx_Oracle.makedsn(host,port,ins_name)
        #     self.db = cx_Oracle.connect(username,passwd,tns)
        #     cx_Oracle.connect()
        # else:
        #     # 创建数据库连接
        #     self.db = pymysql.connect(
        #         host = host,
        #         port = port,
        #         user = username,
        #         passwd = passwd,
        #         db = ins_name,
        #         charset = 'utf8',
        #         # 加上cursorclass之后就可以直接把字段名捞出来，和字段值组成键值对的形式
        #         cursorclass = pymysql.cursors.DictCursor
        #     )
        db_config = set_db_config(db_type,db_name,env)
        if self.db_type == "mysql":
            self.db = PooledDB(pymysql,5,**db_config).connection()
        elif self.db_type == "sqlite":
            self.db = PooledDB(sqlite3, 5, **db_config).connection()
        elif self.db_type == "redis":
            pool = redis.ConnectionPool(**db_config)
            self.db = redis.Redis(connection_pool=pool)
        else:
            self.db = PooledDB(cx_Oracle, 5, **db_config).connection()
        # 创建游标
        if self.db_type != "redis":
            self.cur = self.db.cursor()

    def __new__(cls, *args, **kwargs):
        '''
        实现单例模式
        :param args:
        :param kwargs:
        :return:
        '''
        if not hasattr(cls,"_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    #获取一条数据
    def search_one(self,sql,param=None):
        if self.db_type == "sqlite":
            self.cur.execute(sql)
            res = self.cur.fetchone()
        elif self.db_type == "redis":
            #注意此时的sql并不是sql语句了，而是一个key值
            res = self.db.get(sql).decode("utf-8")
        else:
            self.cur.execute(sql,param)
            res = self.cur.fetchone()
        if res and (self.db_type == 'oracle' or self.db_type == "sqlite"):
            res = self.makeDictFactory(*res)
        return res

    #获取所有数据
    def search_all(self,sql,param=None):
        self.cur.execute(sql,param)
        res = self.cur.fetchall()
        if self.db_type == 'oracle':
            res = self.makeDictFactory(*res)
        return res

    #新增/删除/更新数据
    def sql_DML(self,sql,param=None):
        try:
            self.cur.execute(sql,param)
            self.db.commit()
        except:
            self.db.rollback()

    #将返回的结果和字段名映射成字典
    def makeDictFactory(self,*args):
        columnNames = [d[0] for d in self.cur.description]
        if isinstance(args[0],list):
                return [dict(z) for z in [zip(columnNames,data) for data in args]]
        return dict(zip(columnNames,args))



    #关闭游标和数据库连接
    def close(self):
        self.cur.close()
        self.db.close()

if __name__ == '__main__':
    # opera_db = OperationDB('sqlite',"person_manager_record.db")
    # res = opera_db.search_one('select `col_1`,`col_2` from `person_table` where `col_1`="48729894";')
    # # # res = opera_db.search_one("select user_name,telphone,source,status from t_activity_order WHERE source='PAWH'" )
    # print(res,type(res))
    opera_db = OperationDB(db_name="uniubi_bi_device")
    for i in range(10):
        print(opera_db.search_one("select COUNT(*) from  device_group where group_id=1 and group_floor_id={} and group_member_id is  null  and is_delete=0;".format(i+1)))
        # print(opera_db.search_one("SELECT count(*) from group_portal where group_id=1 and group_floor_id={}  and is_delete=0 and group_member_id is  null and type=2;".format(i+1)))
        # print(opera_db.search_one("SELECT count(*) from group_portal where group_id=1 and group_floor_id={}  and is_delete=0  and type=3;".format(i+1)))
        # print(opera_db.search_one("SELECT count(*) from group_member_floor where group_floor_id={}  and is_delete=0;".format(i+1)))
    # # res1 = opera_db.makeDictFactory(*res)
    # # print(type(res1))
    # opera_db.close()
    # a = ["col1","col2","col3"]
    # b = [[1,2,3],[4,5,6]]
    # r = [dict(z) for z in [(zip(a,data)) for data in b]]
    # print(r)
    # db = sqlite3.connect(r"E:\工具\person_manager_record.db")
    # cur = db.cursor()
    # cur.execute('select `col_1`,`col_2` from `person_table` where `col_1`="48729894";')
    # print(cur.fetchone())