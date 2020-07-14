from util.read_ini import ReadIni
from jsonpath_rw import parse,jsonpath

class HandleSaveValue:
    def get_save_field(self,save_value):
        '''
        获取要存储的字段,如果有多个字段用;分隔
        :return:
        '''
        if save_value:
            save_value_list = save_value.split(";")
            if "=" in save_value:
               for i,value in enumerate(save_value_list):
                    value_list = value.split("=")
                    save_value_list[i] = value_list
            return save_value_list  # ;用于分隔多个字段
        else:
            print("没有需要存储的变量")
            return None


    def save_response_data(self,response_data,save_value):
        '''
        取出需要存储的多个字段
        :return:
        '''
        save_value_list = self.get_save_field(save_value)
        if save_value_list:
            read_i = ReadIni()
            for i, save_value in enumerate(save_value_list):
                if save_value:
                    #如果是个list,说明传了变量名
                    if isinstance(save_value,list):
                        save_value_p = parse(save_value[1])
                        madle = save_value_p.find(response_data)
                        res = [match.value for match in madle][0]
                        read_i.write_data(save_value[0], str(res), "variable")
                    else:
                    #如果不传变量名，则以要存储的内容命名变量
                        save_value_p = parse(save_value)
                        madle = save_value_p.find(response_data)
                        res = [match.value for match in madle][0]
                        read_i.write_data(save_value,str(res),"variable")


if __name__ == "__main__":
    h = HandleSaveValue()
    h.save_response_data({"data":{"id1":12345}},"cs=data.id1")
    # print(h.get_save_field("data.id"))