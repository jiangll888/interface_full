from util.opera_db import OperationDB
import re

def change_caseid(caseid1,caseid2,i):
    TABLE_NAME = "cases_copy"
    opera_db = OperationDB()
    sql = "select case_id,post_action from {} where case_id>='{}' and case_id<='{}';".format(TABLE_NAME,caseid1,caseid2)
    data = opera_db.search_all(sql)
    print(data)
    for item in data:
        caseid = item.get("case_id")
        num = int(re.search("\d+(?=_)",caseid).group())
        num1 = num + i
        caseid_new = re.sub(str(num), str(num1), caseid)
        post_action = item.get("post_action")
        if post_action and "case_id" in post_action and (post_action.split("=")[1]>=caseid1 and post_action.split("=")[1]<=caseid2):
            num2 = int(re.search("\d+(?=_)",post_action.split("=")[1]).group())
            num3 = num2 + i
            post_action_new = re.sub(str(num2), str(num3), post_action)
        else:
            post_action_new = post_action
        sql1 = "update {} set case_id='{}',post_action='{}' where case_id='{}';".format(TABLE_NAME,caseid_new,post_action_new,caseid)
        opera_db.sql_DML(sql1)

if __name__ == "__main__":
    change_caseid('bs95_group_updataMap','bs99_group_portal_bindinginfo',1)
