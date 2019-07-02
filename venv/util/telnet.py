import socket
import os,sys,select
import time

class Telnet():
	def __init__(self,host,port,buffer):
		self.host = host
		self.port = port
		self.buffer = buffer
	def telnet(self):
		try :
			self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.s.connect((self.host,self.port))
			return self.s.recv(self.buffer)
		except Exception as e:
			print(e)
	def send(self,command):
		self.command = command
		while True:
			msg = self.s.recv(self.buffer).decode("utf-8")
			if "login" in msg:
				self.s.send(("root" + "\n").encode('utf-8'))  # 发送数据
			else:
				break
		while True:
			msg = self.s.recv(self.buffer).decode("utf-8")
			if "Password" in msg:
				self.s.send(("" + "\n").encode('utf-8'))  # 发送数据
			else:
				break
		self.s.send((self.command + "\n").encode('utf-8'))
		self.data = ""
		while True:
			value1,value2,value3 = select.select([self.s],[],[],1)
			if len(value1):
				# try :
					data_recv = self.s.recv(self.buffer)
					self.data = self.data + data_recv.decode("utf-8")
					if not data_recv:
						break
				# except Exception as e:
				# 	print(e)
			else :
				break
		print(self.data,type(self.data))
		return self.data
	def close(self):
		self.s.close()



class Log():
	def __init__(self,path,filename):
		self.path = path
		self.filename = filename
		
	def mkdir(self):
		time1 = str(time.strftime("%Y-%m-%d",time.localtime()))
		self.basedir = "%s/%s" %(self.path,time1)
		if os.path.exists(self.basedir):
			pass
		else:
			os.makedirs(self.basedir)
		self.fileid = open(self.basedir + "/" + self.filename,"a")
	def log(self,content):
		try :
			self.mkdir()
			self.fileid.write(content)
		except Exception as e:
			print(e)
	def close(self):
		self.fileid.flush
		self.fileid.close()


#class UserManagent():
	#def 




if __name__ == "__main__":
        tn = Telnet("192.168.19.107",23,1024)
        log = Log("../LOG","log.txt")
        m = tn.telnet()
        n = tn.send("ls\n")
        log.log(n)
        # o = tn.send("admin\n")
        # log.log(o)
        # a = tn.send("en\n")
        # log.log(a)
        # b = tn.send("show ver\n")
        # e=b.split('\n')[5].split(':')[1].split()[0]
        # log.log(b)
        # c = tn.send("debug\n")
        # log.log(c)
        # d = tn.send("center management server ip 192.168.1.9 port 50001\n")
        tn.close()
        log.close()
       

