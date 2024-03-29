import json

class HandleListOrDict:
    def handle_value(self,data):
        if data and (isinstance(data,dict) or isinstance(data,list)):
            # for key,value in data.items():
            #     if isinstance(value,dict) or isinstance(value,list):
            #         data[key] = json.dumps(data[key],ensure_ascii=False)
            #显示中文需要加ensure_ascii=False
            return json.dumps(data,ensure_ascii=False)

if __name__ == "__main__":
    h = HandleListOrDict()
    data = {
        "1":{
            "2":"3",
            "3":"4"
        }
    }
    d = h.handle_value(data)
    print(d,type(d))