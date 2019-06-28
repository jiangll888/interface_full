from config import settings
from util.opera_db import OperationDB

class Count:
    def __init__(self):
        self.op_db = OperationDB()

    def count(self):
        pass_count = fail_count = 0
        result = self.op_db.search_all(settings.GET_RESULT_SQL)
        for d in result:
            if  d.get(settings.RESULT) == "pass":
                pass_count += 1
            elif d.get(settings.RESULT) == "fail":
                fail_count +=1
        return  str(pass_count),str(fail_count)


if __name__ == "__main__":
    d = Count()
    r = d.count()
    print(r)
