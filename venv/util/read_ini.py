import configparser

class ReadIni:
    def __init__(self,filename=None):
        if filename == None:
            self.filename = "../config/global_var.ini"
        else:
            self.filename = filename
        self.config = self.read_data()

    def read_data(self):
        config = configparser.ConfigParser()
        config.read(self.filename,encoding="utf-8")
        return config

    def get_value(self,key,section=None):
        if section == None:
            section = "variable"
        try:
            element_key = self.config.get(section,key)
        except:
            print("没有这个元素")
            element_key = None
        return element_key

    def write_data(self,key,value,section=None):
        if section == None:
            section = "variable"
            self.config.set(section,key,value)
        else:
            if section in self.config.sections():
                self.config.set(section,key,value)
            else:
                self.config.add_section(section)
                self.config.set(section,key,value)
        with open(self.filename,"w",encoding="utf-8") as fp:
            self.config.write(fp)

if __name__ == "__main__":
    r = ReadIni()
    r.write_data("username1","test111","variable")
    print(r.get_value("test"))